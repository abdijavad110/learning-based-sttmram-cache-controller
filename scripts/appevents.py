import sim

class AppEvents:
  def hook_application_start(self, appid):
    print '[APP]', appid, 'start'
    sim.mpd.marker(-1, -1, appid, 0, "application start")

  def hook_application_exit(self, appid):
    print '[APP]', appid, 'exit'
    sim.mpd.marker(-1, -1, appid, 0, "application exit")

sim.util.register(AppEvents())
