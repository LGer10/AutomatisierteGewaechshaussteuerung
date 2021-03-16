from MicroWebSrv2 import *
from time         import sleep
import sys


pyhtmlTemplateMod = MicroWebSrv2.LoadModule('PyhtmlTemplate')
pyhtmlTemplateMod.ShowDebug = True

"""
xasPool  = XAsyncSocketsPool()
#srvHttp  = MicroWebSrv2()
srvHttps = MicroWebSrv2()

#srvHttps.EnableSSL( certFile = 'SSL-Cert/openhc2.crt',
#                    keyFile  = 'SSL-Cert/openhc2.key' )

#srvHttp.SetEmbeddedConfig()
#srvHttp._slotsCount = 4

srvHttps.SetEmbeddedConfig()
srvHttps._slotsCount = 4

#srvHttp .StartInPool(xasPool)
srvHttps.StartInPool(xasPool)

xasPool.AsyncWaitEvents(threadsCount=1)

@WebRoute(GET, '/')
def hello_world(microWebSrv2, request):
   return 'Hello Tutorialspoint'

@WebRoute(GET, '/test')
def RequestTest(microWebSrv2, request) :
 pass

@WebRoute(GET, '/my-resource')
def RequestHandler1(microWebSrv2, request) :
    pass

try :
    while True :
        sleep(1)
except KeyboardInterrupt :
    #srvHttp.Stop()
    srvHttps.Stop()
    xasPool .StopWaitEvents()

"""