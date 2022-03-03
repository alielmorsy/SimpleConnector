using System.Net;
using System.Net.Sockets;
using System.Text;
using SimpleConnector.Exceptions;

namespace SimpleConnector;

public class Connector : IConnector
{
    private Socket _socket;

    public Connector()
    {
    }


    public void Connect(int port)
    {
        if (_socket != null)
        {
            throw new ConnectionException("API Connected Already");
        }


        var ipAddress = IPAddress.Parse("127.0.0.1");
        _socket = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
        try
        {
            _socket.Connect(ipAddress, port);

            _socket.Blocking = false;
        }
        catch (Exception e)
        {
            throw new ConnectionException("Failed to connect to python API: with error" + e);
        }
    }

    public void SendMessage(string message)
    {
        try
        {
            _socket.Send(Encoding.Default.GetBytes(message));
        }
        catch (SocketException e)
        {
            throw new ConnectionException("Failed to send message. Connection Aborted");
        }
    }

    public string? WaitForMessage()
    {
        var ms = new MemoryStream();
        while (_socket.Available > 0)
        {
            var buffer = new byte[1024];
            _socket.Receive(buffer);    
        }
        ms.Close();
        return Convert.ToString(ms.ToArray());
    }

    public void Dispose()
    {
        _socket.Dispose();
        GC.SuppressFinalize(this);
        
    }

    
}