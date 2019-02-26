---
layout: post
title:  "Spotify Knows What TV You Have"
date: 2017-04-30 12:00:00 +0100
time_to_read: 2
has_code: true
redirect_from: writing/spotify-knows-what-tv-you-have
---

I was playing around with [WireShark](https://www.wireshark.org/) today and noticed something strange. My computer, despite running [NordVPN](https://nordvpn.com) and sending all web traffic over [OpenVPN](https://en.wikipedia.org/wiki/OpenVPN), was sending some HTTP requests.

Here's one of the HTTP requests in question.

{% highlight HTTP %}
GET /dd.xml HTTP/1.1
Host: XXX.XXX.XXX.XXX:43214
User-Agent: Spotify/105300758 OSX/0 (MacBookPro10,1)
Keep-Alive: 0
Connection: keep-alive
Accept-Encoding: gzip
{% endhighlight %}

I quickly noticed that the request's (redacted) destination IP was on my local network, so I let my VPN off the hook. I also noticed that it was the [Spotify](https://www.spotify.com/uk/) app (version 1.0.53.758) on my MacBook Pro soliciting this information from another machine on my network.

The actual HTTP response was an XML file of the following form.

{% highlight xml %}
<root xmlns="urn:schemas-upnp-org:device-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>
  <device>
    <deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>
    <friendlyName>...</friendlyName>
    <manufacturer>Sony Corporation</manufacturer>
    <manufacturerURL>http://www.sony.net/</manufacturerURL>
    <modelDescription>BRAVIA</modelDescription>
    <modelName>...</modelName>
    <UDN>...</UDN>
    <serviceList>
      <service>
      <serviceType>urn:dial-multiscreen-org:service:dial:1</serviceType>
      <serviceId>urn:dial-multiscreen-org:serviceId:dial</serviceId>
      <SCPDURL>/DIALSCPD.xml</SCPDURL>
      <controlURL>/upnp/control/DIAL</controlURL>
      <eventSubURL/>
      </service>
    </serviceList>
    <av:X_DIALEX_DeviceInfo xmlns:av="urn:schemas-sony-com:av">
      <av:X_DIALEX_AppsListURL>
        http://XXX.XXX.XXX.XXX:80/DIAL/sony/applist
      </av:X_DIALEX_AppsListURL>
      <av:X_DIALEX_DeviceType>Android_TV_DIAL_v2.0.0</av:X_DIALEX_DeviceType>
    </av:X_DIALEX_DeviceInfo>
  </device>
</root>
{% endhighlight %}

Huh? That's (redacted) information about my Sony TV (which never works properly... *shakes fist at Sony*). What is going on?

Some further Googling explained it. My TV hosts a [Universal Plug and Play](https://en.wikipedia.org/wiki/Universal_Plug_and_Play) (UPNP) service that allows other devices to discover it's presence. UPNP is used for stuff like wireless printers, gaming consoles, TVs, etc. It is possible to configure your router to [disable UPNP](https://www.forbes.com/sites/andygreenberg/2013/01/29/disable-a-protocol-called-upnp-on-your-router-now-to-avoid-a-serious-set-of-security-bugs/#5087d0a976b4), as many have done due to [vulnerabilities](https://en.wikipedia.org/wiki/Universal_Plug_and_Play#Problems_with_UPnP), but that might result in a loss of functionality.

Spotify probably aren't using this device information for anything malicious. However, it strikes me that third parties (think Google, Amazon and others) can discover what devices you have in your home and could use this to improve their ad targeting.
