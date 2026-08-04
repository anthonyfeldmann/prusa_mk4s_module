#! /usr/bin/env python3
"""Prusa MK4S Rest Node."""

from typing import Any, Optional
from typing_extensions import Annotated
from pathlib import Path

from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode

import prusa_driver
from secrets_loader import get_secrets

class PrusaNodeConfig(RestNodeConfig):
    """Config for Prusa node."""
    prusa_ip: Optional[str] = None
    prusa_api_key: Optional[str] = None

class PrusaNode(RestNode):
    """Node module for Prusa MK4S."""
    
    config: PrusaNodeConfig = PrusaNodeConfig()
    config_model = PrusaNodeConfig

    def startup_handler(self) -> None:
        """Initialize node."""
        self.logger.log("Starting Prusa Node")
        
        secrets = get_secrets()
        
        # Fallback to secrets if not provided dynamically in the MADSci config
        if not self.config.prusa_ip:
            self.config.prusa_ip = secrets.get("prusa_ip")
        if not self.config.prusa_api_key:
            self.config.prusa_api_key = secrets.get("prusalink_key")
            
        if not self.config.prusa_ip or not self.config.prusa_api_key:
            raise ValueError("Prusa IP or API key is missing from config and secrets")

        prusa_driver.PRINTER_IP = self.config.prusa_ip
        prusa_driver.PRUSALINK_KEY = self.config.prusa_api_key
        
        self.startup_has_run = True
        self.logger.info("Prusa node started")

    def shutdown_handler(self) -> None:
        """Cleanly shuts down the node."""
        self.logger.log("Ending Prusa node")
        self.shutdown_has_run = True

    def state_handler(self) -> None:
        """Returns the current node state."""
        self.node_state = {"status": "ready"}

    @action(name="slice_and_print", description="Slice a given STL file and print it")
    def slice_and_print(
        self, stl_path: Annotated[Path, "Absolute path to the STL file"]
    ) -> dict[str, Any]:
        """Takes an STL path, slices it to .bgcode, and runs the printer."""
        self.logger.log(f"Executing print job for STL: {stl_path.resolve()}")
        
        try:
            # Passes the STL directly to the run_stl_print function as a string
            success = prusa_driver.run_stl_print(str(stl_path))
            
            if success:
                self.logger.log("Print job successfully completed.")
                return {"status": "succeeded", "stl_path": str(stl_path)}
            else:
                raise Exception("PrusaLink rejected the print job or encountered an error.")
                
        except Exception as err:
            self.logger.error(f"Action failed: {err}")
            raise

if __name__ == "__main__":
    PrusaNode().start_node()
