// This autogenerated skeleton file illustrates how to build a server.
// You should copy it to another filename to avoid overwriting it.

#include "rpc.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

class rpcHandler : virtual public rpcIf {
 public:
  rpcHandler() {
    // Your initialization goes here
  }

  void sendCommand(std::string& _return, const std::string& command) {
    // Your implementation goes here
    printf("sendCommand\n");
  }

};

int main(int argc, char **argv) {
  int port = 9090;
  ::std::shared_ptr<rpcHandler> handler(new rpcHandler());
  ::std::shared_ptr<TProcessor> processor(new rpcProcessor(handler));
  ::std::shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  ::std::shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  ::std::shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}

