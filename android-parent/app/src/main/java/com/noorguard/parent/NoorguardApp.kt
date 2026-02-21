package com.noorguard.parent

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class NoorguardApp : Application() {
    
    override fun onCreate() {
        super.onCreate()
        // Initialize application
    }
}
