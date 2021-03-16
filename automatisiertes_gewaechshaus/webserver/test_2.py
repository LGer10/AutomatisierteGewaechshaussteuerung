from MicroWebSrv2 import *
import ssl
import socket

ssl.SSLContext

xasPool  = XAsyncSocketsPool()
srvHttps  = MicroWebSrv2()

srvHttps.EnableSSL( certFile = 'SSL-Cert/certificate.crt',
                    keyFile  = 'SSL-Cert/privateKey.key' )

srvHttps.SetEmbeddedConfig()
srvHttps._slotsCount = 4
srvHttps.StartInPool(xasPool)
xasPool.AsyncWaitEvents(threadsCount=1)

try :
    while True :
        sleep(1)
except KeyboardInterrupt :
    srvHttp .Stop()
    srvHttps.Stop()
    xasPool .StopWaitEvents()