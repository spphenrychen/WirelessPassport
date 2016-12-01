package com.rongson.wirelesspassport;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pDeviceList;
import android.net.wifi.p2p.WifiP2pManager;
import android.util.Log;

/**
 * Created by RongSonHo on 11/21/16.
 */
public class WiFiDirectBroadcastReceiver extends BroadcastReceiver {
    private WifiP2pManager mManager;
    private WifiP2pManager.Channel mChannel;
    private MainActivity mActivity;
    private String TAG="WiFiDirectBroadcastReceiver";

    public WiFiDirectBroadcastReceiver(WifiP2pManager manager, WifiP2pManager.Channel channel, MainActivity activity) {
        super();
        this.mManager = manager;
        this.mChannel = channel;
        this.mActivity = activity;
        Log.e(TAG,"in Constructor");
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();

        if (WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION.equals(action)) {
            // Check to see if Wi-Fi is enabled and notify appropriate activity

            int state = intent.getIntExtra(WifiP2pManager.EXTRA_WIFI_STATE, -1);
            Log.e(TAG,"onReceive:"+state);
            if (state == WifiP2pManager.WIFI_P2P_STATE_ENABLED) {
                // Wifi P2P is enabled
                Log.e(TAG,"state=WIFI_P2P_STATE_ENABLED");
            } else {
                // Wi-Fi P2P is not enabled
                Log.e(TAG,"state!=WIFI_P2P_STATE_ENABLED");
            }
        } else if (WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION.equals(action)) {
            // Call WifiP2pManager.requestPeers() to get a list of current peers
            Log.e(TAG,"onReceive: WIFI_P2P_PEERS_CHANGED_ACTION");
            mManager.requestPeers(mChannel, new WifiP2pManager.PeerListListener() {

                public void onPeersAvailable(WifiP2pDeviceList peers) {

                    mActivity.displayPeers(peers);
                }
            });

        } else if (WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION.equals(action)) {
            // Respond to new connection or disconnections
            Log.e(TAG,"onReceive: WIFI_P2P_CONNECTION_CHANGED_ACTION");


        } else if (WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION.equals(action)) {
            // Respond to this device's wifi state changing
            Log.e(TAG,"onReceive: WIFI_P2P_THIS_DEVICE_CHANGED_ACTION");
        }
    }

}
