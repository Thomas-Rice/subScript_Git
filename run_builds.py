
import os
import tempfile
import sys
import subprocess








def InstallDMG(dmgPath, volumeLabel='TEST', **kw):
  """
  Mounts a .dmg, then finds the .pkg inside it and installs to a temporary
  volume. Returns a TemporaryVolume object thats the installed volume.
  """
  #where to mount the package image
  pkgVolume = tempfile.mkdtemp(prefix='dmgMount_', dir=os.getcwd())
  os.rmdir(pkgVolume)
  # packageMaker = kw.get("packageMaker", True)
  #hdiutil sometimes fails to mount properly, let it try a few times...

  # if not packageMaker:
  #   #Turn the dmg into a cdr, because then we get around the EULA agreement.
  #   (handle, cdrFile) = tempfile.mkstemp(dir = os.getcwd(), prefix="tempImg", suffix=".cdr")
  #   os.close(handle)
  #   os.remove(cdrFile)
  #   tmpCdr = TemporaryFile(cdrFile)
  #   RunCmd(cmd="/usr/bin/hdiutil convert " + dmgPath + " -format UDTO -o " + cdrFile)
  #   RunCmd(cmd="hdiutil attach -nobrowse -noverify -noautoopen -mountpoint " + pkgVolume + " \"" + cdrFile + "\"")
  #   apps = [entry for entry in os.listdir(pkgVolume) if entry.endswith(".app")]
  #   installDir = kw["installDir"]
  #   for i in apps:
  #     appPath = os.path.join(pkgVolume, i)
  #     shutil.copytree(appPath, os.path.join(installDir,i), True)
  #   RunCmd("hdiutil detach " + pkgVolume + " -force -verbose")
  #   tmpCdr.close()
  #   return TemporaryFolder(installDir)

  cmd = ('hdiutil attach -mountpoint','/Users/Tom/Downloads/Nuke', dmgPath)
  subprocess.call([cmd, shell=True])


  #look in the mounted volume for the .pkg file
  packages = [entry for entry in os.listdir(pkgVolume) if entry.endswith(".pkg")]
  if len(packages) != 1:
    subprocess.call(["hdiutil detach " + pkgVolume + " -force"])

    raise RuntimeError("Can't find right package in " + pkgVolume)



  

  package = os.path.join(pkgVolume, packages[0])
  #where to install the package to
  tempVol = TemporaryVolume(volumeLabel)
  destVolume = tempVol.volume
  RunCmd("sudo installer -pkg %(package)s -verbose  -target %(target)s" % {"package": package, "target": destVolume}, 240)
  #clean up installer package dmg mount
  RunCmd("hdiutil detach " + pkgVolume + " -force -verbose")
  # #Pre-emptively kill the PluginInstaller to make the teardown simpler.
  # (status,output) = commands.getstatusoutput("ps ax | grep PluginInstaller | grep Volumes | grep -v grep")
  # for line in output.strip().split("\n"):
  #   if len(line)>0:
  #     try:
  #       pid = line.split()[0]
  #     except:
  #       print "line:\n%s" % line
  #       raise
  #     RunCmd("sudo kill %s" % pid, 20, False)
  # return tempVol



class ScopedObject(object):
  def __init__(self):
    self.closed = False
    self.childScopedObjects = []
    # Temporarily commented for testing...atexit.register(ScopedObject.close, self)
  def addFolderToClean(self, folder):
    self.addChildScopedObject(TemporaryFolder(folder))
  def addFileToClean(self, filename):
    self.addChildScopedObject(TemporaryFile(filename))
  def addChildScopedObject(self, child):
    if self.closed:
      raise RuntimeError("Can't add a child object to a ScopedObject that's already been closed.")
    self.childScopedObjects.append(child)
  def close(self):
    if not self.closed:
      self.closed = True
      #Close the children first
      for i in self.childScopedObjects:
        try:
          i.close()
        except Exception, e:
          print "CLEANUP ERROR: *** Caught exception: %s: %s\n" % (e.__class__, str(e))
          exc_type, exc_value, exc_traceback = sys.exc_info()
          traceback.print_tb(exc_traceback, None, sys.stdout)
      self.cleanUp()
  def cleanUp(self):
    pass # Pure virtual
  def __del__(self):
    self.close()

class TemporaryFolder(ScopedObject):
  def __init__(self, folderName):
    ScopedObject.__init__(self)
    self.name = folderName
    FnFileUtils.MkDir_p(folderName)
  def cleanUp(self):
    if os.environ.has_key("FN_TEST_DEBUG_LEAVE_FILES"):
      return
    FnFileUtils.FnDeleteFolder(self.name)

class TemporaryFile(ScopedObject):
  def __init__(self, fileName):
    ScopedObject.__init__(self)
    self.name = fileName
  def cleanUp(self):
    if os.environ.has_key("FN_TEST_DEBUG_LEAVE_FILES"):
      return
    FnFileUtils.FnDeleteFile(self.name)

def MakeScopedTemporaryFile(parentScopedObject, suffix="", prefix="tmp"):
  (handle, pathToFile) = tempfile.mkstemp(dir=os.getcwd(), suffix=suffix, prefix=prefix)
  os.close(handle)
  parentScopedObject.addChildScopedObject(TemporaryFile(pathToFile))
  return pathToFile




class TemporaryVolume(ScopedObject):
  """Container for creating .dmg based volumes on mac, and clean up after"""
  def __init__(self, volName):
    ScopedObject.__init__(self)
    self.imageFile = tempfile.mktemp(prefix=volName + '_', suffix=".dmg", dir=os.getcwd())
    #get the volume name from the temp image name
    self.volName = os.path.splitext(os.path.basename(self.imageFile))[0]
    self.volume = os.path.join("/Volumes", self.volName)
    RunCmd("hdiutil create -megabytes 2000 -attach -volname " + self.volName + " -fs HFS+ " + self.imageFile, 120)
  def cleanUp(self):
    if os.path.exists(self.volume):
      os.system("hdiutil detach " + self.volume + " -force")
    time.sleep(1)
    os.remove(self.imageFile) 
    
    
InstallDMG(' Nuke10.0v1.001291b-mac-x86-release-64.dmg')

(['hdiutil attach -mountpoint /Users/Tom/Downloads/Nuke', 'Nuke10.0v1.001291b-mac-x86-release-64.dmg'])

['hdiutil attach -mountpoint "/Users/Tom/Downloads/Nuke" Nuke10.0v1.001291b-mac-x86-release-64.dmg', shell=True]