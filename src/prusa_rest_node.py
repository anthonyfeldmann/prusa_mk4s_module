#! /usr/bin/env python3
"""Prusa MK4S Rest Node"""

from typing import Optional
from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode
from typing_extensions import Annotated

import prusa_driver

class PrusaNodeConfig(RestNodeConfig):
    """Configuration for the Prusa node module."""
    prusa_ip: Optional[str] = None
    prusa_api_key: Optional[str] = None


class PrusaNode(RestNode):
    """Node module for Prusa 3D """
    config: PrusaNodeConfig = PrusaNodeConfig()
    config_model = PrusaNodeConfig

    def startup_handler(self) -> None:
        """Initializes the node."""
        self.logger.log("Initializing Prusa MK4S node")
        
        if not self.config.prusa_ip or not self.config.prusa_api_key:
            raise ValueError("Prusa IP or API key missing from config")

        # Push credentials directly to driver
        prusa_driver.PRINTER_IP = self.config.prusa_ip
        prusa_driver.PRUSALINK_KEY = self.config.prusa_api_key
        
        self.startup_has_run = True
        self.logger.info("Prusa node created")

    def shutdown_handler(self) -> None:
        """Cleanly shuts down the node."""
        self.logger.log("Shutting down Prusa node...")
        self.shutdown_has_run = True

    def state_handler(self) -> None:
        """Reports the node's current status to the WEI orchestrator."""
        self.node_state = {"status": "ready"}

    @action(name="slice_and_print", description="Run parametric generation and print")
    def slice_and_print(
        self, length: Annotated[float, "Parametric length in mm"]
    ) -> dict:
        """Triggers the physical printer via your driver."""
        self.logger.log(f"Executing print job for length: {length}mm")
        
        try:
            # Assumes your driver now returns True on success and False on failure
            success = prusa_driver.run_parametric_loop(length)
            
            if success:
                self.logger.log("Print job successfully pushed to PrusaLink.")
                return {"status": "succeeded", "length": length}
            else:
                raise Exception("PrusaLink rejected the print job.")
                
        except Exception as err:
            self.logger.error(f"Action failed: {err}")
            raise


if __name__ == "__main__":
    PrusaNode().start_node()
