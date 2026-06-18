#! /usr/bin/env python3
"""OpenCV Camera Rest Node."""

from typing import Any
from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode

import camera_driver

class CameraNodeConfig(RestNodeConfig):
    """Config for Camera node."""
    # Add any specific camera settings here if needed, 
    # otherwise it inherits the standard IP/Port config.
    pass

class CameraNode(RestNode):
    """Node module for USB Camera."""
    config: CameraNodeConfig = CameraNodeConfig()
    config_model = CameraNodeConfig

    def startup_handler(self) -> None:
        """Initialize node."""
        self.logger.log("Starting Camera Node")
        self.startup_has_run = True

    def shutdown_handler(self) -> None:
        """Cleanly shuts down the node."""
        self.logger.log("Shutting down Camera Node")
        self.shutdown_has_run = True

    def state_handler(self) -> None:
        """Returns the current node state."""
        # You could add a check here to ensure /dev/video0 is accessible
        self.node_state = {"status": "ready"}

    @action(name="measure_drop", description="Takes a picture and measures the fluid drop")
    def measure_drop(self) -> dict[str, Any]:
        """Triggers the OpenCV driver and returns the physical height."""
        self.logger.log("Executing measurement...")
        
        try:
            # Trigger your custom driver
            height = camera_driver.get_single_measurement(
                target_bucket=3, total_buckets=5, pixels_per_mm=3.2
            )
            
            if height is not None:
                self.logger.log(f"Measurement successful: {height}mm")
                return {"status": "succeeded", "measurement": height}
            else:
                raise Exception("Camera failed to capture or process image.")
                
        except Exception as err:
            self.logger.error(f"Action failed: {err}")
            raise

if __name__ == "__main__":
    import sys
    
    # Automatically set the port to 2000 for the camera
    if "--port" not in sys.argv:
        sys.argv.extend(["--port", "2000"])
        
    CameraNode().start_node()