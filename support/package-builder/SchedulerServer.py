import flask
from Scheduler import Scheduler
from constants import constants
from Logger import Logger

SUCCESS=200
NO_CONTENT=204
BAD_REQUEST=400
NOT_ACCEPTABLE=406

app = flask.Flask(__name__)
mapPackageToCycle = {}

logger = Logger.getLogger('werkzeug', constants.logPath, constants.logLevel)

def shutdownServer():
        logger.disabled = False
        logger.info("Shutting down server......")
        stopServer = flask.request.environ.get('werkzeug.server.shutdown')
        if stopServer is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        stopServer()

def buildCompleted():
    if not Scheduler.isAnyPackagesCurrentlyBuilding():
        return True
    return False

@app.route('/package/', methods=['GET'])
def getNextPkgToBuild():
    logger.disabled = False
    pkg = Scheduler.getNextPackageToBuild()
    if not pkg:
        ## if no package is left to schedule and no package is currently building
        ## our build is complete either all of them passed or some failed
        if buildCompleted():
            logger.info("Package build completed...")
            shutdownServer()
        logger.disabled = True
        return '', NO_CONTENT

    logger.info("Scheduling package %s"%pkg)
    logger.disabled = True
    return pkg, SUCCESS

@app.route('/notifybuild/', methods=['POST'])
def notifyPackageBuildCompleted():
    logger.disabled = False
    if 'status' not in flask.request.json or 'package' not in flask.request.json:
        return {'message', 'missing package or status in request'}, BAD_REQUEST

    if flask.request.json['status'] == 0:
        Scheduler.notifyPackageBuildCompleted(flask.request.json['package'])
        logger.info("Build Success %s"%flask.request.json['package'])
    elif flask.request.json['status'] == -1:
        Scheduler.notifyPackageBuildFailed(flask.request.json['package'])
        logger.info("Build Failed %s"%flask.request.json['package'])
    else:
        return {'message', 'wrong status'}, NOT_ACCEPTABLE
    logger.disabled = True
    return {'message': 'master notified successfully'}, SUCCESS

@app.route('/donelist/', methods=['GET'])
def getDoneList():
    doneList = Scheduler.getDoneList()
    return flask.jsonify(packages=doneList), SUCCESS


@app.route('/mappackagetocycle/', methods=['GET'])
def getMapPackageToCycle():
    return mapPackageToCycle, SUCCESS

@app.route('/constants/', methods=['GET'])
def getConstants():
    constant_dict = {}
    constant_dict['specPath'] = constants.specPath
    constant_dict['sourcePath'] = constants.sourcePath
    constant_dict['rpmPath'] = constants.rpmPath
    constant_dict['sourceRpmPath'] = constants.sourceRpmPath
    constant_dict['topDirPath'] = constants.topDirPath
    constant_dict['logPath'] = constants.logPath
    constant_dict['logLevel'] = constants.logLevel
    constant_dict['dist'] = constants.dist
    constant_dict['buildNumber'] = constants.buildNumber
    constant_dict['releaseVersion'] = constants.releaseVersion
    constant_dict['prevPublishRPMRepo'] = constants.prevPublishRPMRepo
    constant_dict['prevPublishXRPMRepo'] = constants.prevPublishXRPMRepo
    constant_dict['buildRootPath'] = constants.buildRootPath
    constant_dict['pullsourcesURL'] = constants.pullsourcesURL
    constant_dict['extrasourcesURLs'] = constants.extrasourcesURLs
    constant_dict['buildPatch'] = constants.buildPatch
    constant_dict['inputRPMSPath'] = constants.inputRPMSPath
    constant_dict['rpmCheck'] = constants.rpmCheck
    constant_dict['rpmCheckStopOnError'] = constants.rpmCheckStopOnError
    constant_dict['publishBuildDependencies'] = constants.publishBuildDependencies
    constant_dict['packageWeightsPath'] = constants.packageWeightsPath
    constant_dict['userDefinedMacros'] = constants.userDefinedMacros
    constant_dict['katBuild'] = constants.katBuild
    constant_dict['tmpDirPath'] = constants.tmpDirPath
    constant_dict['buildArch'] = constants.buildArch
    constant_dict['currentArch'] = constants.currentArch

    return constant_dict, SUCCESS

def startServer():
    ## if no packages to build then return
    if Scheduler.isAllPackagesBuilt():
        return
    logger.info("Starting Server ...")
    try:
        logger.disabled = True
        app.run(host='0.0.0.0', port='80', debug=False, use_reloader=False)
    except Exception as e:
        logger.exception(e)
        logger.error("unable to start server")
        logger.error("")
