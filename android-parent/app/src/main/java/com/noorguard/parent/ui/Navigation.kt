package com.noorguard.parent.ui

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.noorguard.parent.ui.screens.auth.LoginScreen
import com.noorguard.parent.ui.screens.auth.RegisterScreen
import com.noorguard.parent.ui.screens.dashboard.DashboardScreen
import com.noorguard.parent.ui.screens.devices.DevicesScreen
import com.noorguard.parent.ui.screens.children.ChildrenScreen
import com.noorguard.parent.ui.screens.children.ChildDetailScreen
import com.noorguard.parent.ui.screens.analytics.AnalyticsScreen
import com.noorguard.parent.ui.screens.settings.SettingsScreen
import com.noorguard.parent.ui.screens.prayer.PrayerTimesScreen

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Register : Screen("register")
    object Dashboard : Screen("dashboard")
    object Devices : Screen("devices")
    object Children : Screen("children")
    object ChildDetail : Screen("child/{childId}") {
        fun createRoute(childId: String) = "child/$childId"
    }
    object Analytics : Screen("analytics")
    object Settings : Screen("settings")
    object PrayerTimes : Screen("prayer_times")
}

@Composable
fun NoorGuardNavigation(
    navController: NavHostController,
    startDestination: String = Screen.Login.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(Screen.Login.route) {
            LoginScreen(
                onNavigateToRegister = { navController.navigate(Screen.Register.route) },
                onLoginSuccess = {
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Register.route) {
            RegisterScreen(
                onNavigateToLogin = { navController.popBackStack() },
                onRegisterSuccess = {
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Dashboard.route) {
            DashboardScreen(
                onNavigateToDevices = { navController.navigate(Screen.Devices.route) },
                onNavigateToChildren = { navController.navigate(Screen.Children.route) },
                onNavigateToAnalytics = { navController.navigate(Screen.Analytics.route) },
                onNavigateToSettings = { navController.navigate(Screen.Settings.route) },
                onNavigateToPrayer = { navController.navigate(Screen.PrayerTimes.route) }
            )
        }

        composable(Screen.Devices.route) {
            DevicesScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(Screen.Children.route) {
            ChildrenScreen(
                onNavigateToChild = { childId ->
                    navController.navigate(Screen.ChildDetail.createRoute(childId))
                },
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(
            route = Screen.ChildDetail.route,
            arguments = listOf(navArgument("childId") { type = NavType.StringType })
        ) { backStackEntry ->
            val childId = backStackEntry.arguments?.getString("childId") ?: ""
            ChildDetailScreen(
                childId = childId,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(Screen.Analytics.route) {
            AnalyticsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(Screen.Settings.route) {
            SettingsScreen(
                onNavigateBack = { navController.popBackStack() },
                onLogout = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(0) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.PrayerTimes.route) {
            PrayerTimesScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
