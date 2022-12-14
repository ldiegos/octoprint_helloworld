#import octoprint.plugin

# coding=utf-8
from __future__ import absolute_import

__author__ = "Sven Lohrmann <malnvenshorn@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 Sven Lohrmann - Released under terms of the AGPLv3 License"

from math import pi as PI

import octoprint.plugin
from octoprint.settings import valid_boolean_trues
from octoprint.events import Events
from octoprint.util import dict_merge
from octoprint.util.version import is_octoprint_compatible

from .newodometer import NewFilamentOdometer


#class HelloWorldPlugin(octoprint.plugin.StartupPlugin):
#class HelloWorldPlugin(FilamentManagerApi,
#                            octoprint.plugin.StartupPlugin,
#                            octoprint.plugin.ShutdownPlugin,
#                            octoprint.plugin.SettingsPlugin,
#                            octoprint.plugin.AssetPlugin,
#                            octoprint.plugin.TemplatePlugin,
#                            octoprint.plugin.EventHandlerPlugin):


class HelloWorldPlugin(octoprint.plugin.StartupPlugin,
                            octoprint.plugin.ShutdownPlugin,
                            octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.EventHandlerPlugin):

    def on_after_startup(self):
        self._logger.info("Hello World!")

    def __init__(self):
        self.client_id = None
        self.filamentManager = None
        # self.filamentOdometer = None
        self.myFilamentOdometer = None
        self.lastPrintState = None

        self.odometerEnabled = False
        self.pauseEnabled = False
        self.pauseThresholds = dict()

    def on_shutdown(self):
        if self.filamentManager is not None:
            self.filamentManager.close()

    def _printJobPaused(self):
        # do nothing
        pass

    def _printJobResumed(self):
        # do nothing
        pass

    # Softwareupdate hook
    def get_update_information(self):
        return dict(
            filamentmanager=dict(
                displayName="Filament Manager",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="OllisGit",
                repo="OctoPrint-FilamentManager",
                current=self._plugin_version,

                # update method: pip
                #pip="https://github.com/malnvenshorn/OctoPrint-FilamentManager/archive/{target_version}.zip"
                pip="https://github.com/OllisGit/OctoPrint-FilamentManager/releases/latest/download/master.zip"
            )
        )

# Protocol hook
    def filament_odometer(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        # is enabled in plugin settings and is currently prining

        if self.odometerEnabled and self._printer.is_printing():
            # self.filamentOdometer.parse(gcode, cmd)
            self.myFilamentOdometer.processGCodeLine(cmd)

            if self.pauseEnabled and self.check_threshold():
                self._logger.info("Filament is running out, pausing print")
                self._printer.pause_print()


__plugin_pythoncompat__ = ">=2,<8"
#__plugin_implementation__ = HelloWorldPlugin()


def __plugin_load__():
    #if not is_octoprint_compatible(__required_octoprint_version__):
    #    import logging
    #    logger = logging.getLogger(__name__)
    #    logger.error("OctoPrint version is not compatible ({version} required)"
    #                 .format(version=__required_octoprint_version__))
    #    return

    global __plugin_implementation__
    #__plugin_implementation__ = FilamentManagerPlugin()
    __plugin_implementation__ = HelloWorldPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information ,
        "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.filament_odometer
    }
