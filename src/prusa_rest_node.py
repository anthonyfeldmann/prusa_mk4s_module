#! /usr/bin/env python3
"""Prusa MK4S Rest Node."""

from typing import Any, Optional
import requests
import time

from typing_extensions import Annotated

from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode

import prusa_driver


class PrusaNodeConfig(RestNodeConfig):
    """Config for Prusa node."""
    
    prusa_ip: Optional[str] = "146.137.240.52"
    prusa_api_key: Optional[str] = "jjehZqxQ542F9pQ"


class PrusaNode(RestNode):
    """Node module for Prusa MK4S."""
    
    config: PrusaNodeConfig = PrusaNodeConfig()
    config_model = PrusaNodeConfig

    def startup_handler(self) -> None:
        """Initialize node."""
        self.logger.log("Starting Prusa Node")
        
        if not self.config.prusa_ip or not self.config.prusa_api_key:
            raise ValueError("Prusa IP or API key is missing from config")

        # Push credentials directly to your custom driver
        prusa_driver.PRINTER_IP = self.config.prusa_ip
        prusa_driver.PRUSALINK_KEY = self.config.prusa_api_key
        
        self.startup_has_run = True
        self.logger.info("Prusa node started")

    def shutdown_handler(self) -> None:
        """Cleanly shuts down the node."""
        self.logger.log("ending prusa node")
        self.shutdown_has_run = True

    def state_handler(self) -> None:
        """Returns the current node state."""
        self.node_state = {"status": "ready"}

    @action(name="slice_and_print", description="Run parametric generation and print")
    def slice_and_print(
        self, length: Annotated[float, "Parametric length in mm"]
    ) -> dict[str, Any]:
        """Takes a length, generates CAD via Onshape, slices, and runs printer."""
        self.logger.log(f"Executing parametric print job for length: {length}mm")
        
        try:
            # Pass the length directly to your original driver logic
            success = prusa_driver.run_parametric_loop(length)
            
            if success:
                self.logger.log("Print job pushed. Waiting for physical completion...")
                
                status_url = f"http://{self.config.prusa_ip}/api/job"
                headers = {"X-Api-Key": self.config.prusa_api_key}
                
                # --- POLLING LOOP (BLOCKS UNTIL FINISHED) ---
                while True:
                    try:
                        status_response = requests.get(status_url, headers=headers, timeout=10)
                        if status_response.status_code == 200:
                            data = status_response.json()
                            state = data.get("state", "unknown").lower()
                            
                            if state == "finished":
                                self.logger.log("Print has finished successfully.")
                                break
                            elif state in ["cancelled", "error"]:
                                raise Exception(f"Printer reported failure state: {state}")
                                
                    except requests.exceptions.RequestException as e:
                        self.logger.warning(f"Failed to reach PrusaLink during polling: {e}")
                    
                    # Wait 15 seconds before checking again
                    time.sleep(15)
                # ---------------------------------------------
                
                # --- EMBEDDED PRINTER RESET VIA M1200 ---
                self.logger.log("Pushing M1200 command to clear completion screen.")
                command_url = f"http://{self.config.prusa_ip}/api/printer/command"
                
                # Send the M1200 G-code directly over the API
                payload = {"commands": ["M1200"]}
                reset_response = requests.post(command_url, json=payload, headers=headers, timeout=10)
                
                if reset_response.status_code in [200, 204]:
                    self.logger.log("Printer successfully reset to Idle via M1200.")
                else:
                    self.logger.warning(f"Failed to reset printer. Status Code: {reset_response.status_code}")
                # ------------------------------
                
                return {"status": "succeeded", "length": length}
            else:
                raise Exception("PrusaLink rejected the print job.")
                
        except Exception as err:
            self.logger.error(f"Action failed: {err}")
            raise


if __name__ == "__main__":
    # Specify port 
    PrusaNode().start_node()
