package com.noorguard.parent.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = DarkPrimary,
    onPrimary = DarkBackground,
    primaryContainer = EmeraldGreenDark,
    onPrimaryContainer = TextPrimaryDark,
    secondary = DarkSecondary,
    onSecondary = DarkBackground,
    secondaryContainer = GoldDark,
    onSecondaryContainer = TextPrimaryDark,
    tertiary = Gold,
    onTertiary = DarkBackground,
    background = DarkBackground,
    onBackground = TextPrimaryDark,
    surface = SurfaceDark,
    onSurface = TextPrimaryDark,
    surfaceVariant = CardDark,
    onSurfaceVariant = TextSecondaryDark,
    error = Error,
    onError = TextPrimaryDark
)

private val LightColorScheme = lightColorScheme(
    primary = EmeraldGreen,
    onPrimary = SurfaceLight,
    primaryContainer = EmeraldGreenLight,
    onPrimaryContainer = TextPrimaryLight,
    secondary = Gold,
    onSecondary = SurfaceLight,
    secondaryContainer = GoldLight,
    onSecondaryContainer = TextPrimaryLight,
    tertiary = EmeraldGreenDark,
    onTertiary = SurfaceLight,
    background = LightBackground,
    onBackground = TextPrimaryLight,
    surface = SurfaceLight,
    onSurface = TextPrimaryLight,
    surfaceVariant = CardLight,
    onSurfaceVariant = TextSecondaryLight,
    error = Error,
    onError = SurfaceLight
)

@Composable
fun NoorGuardTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
