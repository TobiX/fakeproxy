# fakeproxy

This is a very simple "fake" HTTP proxy server to "trap" clients with broken
network configurations.

## Usage

Run the script as a service (see included systemd service file for an example).

A client needs to be told to use the server as its proxy. In our setup, this
was achieved by the folling haproxy config:

```haproxy
    acl wpad_trap hdr_beg(Host) wpad.
    http-request return status 200 content-type application/x-ns-proxy-autoconfig string "function FindProxyForURL(url, host) { if (url.substring(0, 5) == 'http:') { return 'PROXY 192.168.127.127:3128'; } else { return 'DIRECT'; } }" if wpad_trap
```

## Issues

It seems to be basically impossible to send any (visible) erorrs in response to
`CONNECT` (HTTPS) requests. In some iterations of this script, we sent a
`Proxy-Authenticate` requests, which only confuses users even more (and might
"social engineer" them into disclosing credentials), so it was removed again...
