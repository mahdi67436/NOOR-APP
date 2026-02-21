package com.noorguard.parent.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject
import com.noorguard.parent.ui.theme.*

@HiltViewModel
class RegisterViewModel @Inject constructor() : ViewModel() {
    var firstName by mutableStateOf("")
    var lastName by mutableStateOf("")
    var email by mutableStateOf("")
    var password by mutableStateOf("")
    var confirmPassword by mutableStateOf("")
    var isLoading by mutableStateOf(false)
    var errorMessage by mutableStateOf<String?>(null)
    
    fun register(onSuccess: () -> Unit) {
        if (password != confirmPassword) {
            errorMessage = "Passwords do not match"
            return
        }
        
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                kotlinx.coroutines.delay(1000)
                onSuccess()
            } catch (e: Exception) {
                errorMessage = e.message ?: "Registration failed"
            } finally {
                isLoading = false
            }
        }
    }
}

@Composable
fun RegisterScreen(
    onNavigateToLogin: () -> Unit,
    onRegisterSuccess: () -> Unit,
    viewModel: RegisterViewModel = hiltViewModel()
) {
    val focusManager = LocalFocusManager.current
    var passwordVisible by remember { mutableStateOf(false) }
    var confirmPasswordVisible by remember { mutableStateOf(false) }
    
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(EmeraldGreen, EmeraldGreenDark)
                )
            )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(32.dp))
            
            // Logo and Title
            Text(text = "🛡️", style = MaterialTheme.typography.displayMedium)
            
            Text(
                text = "Create Account",
                style = MaterialTheme.typography.headlineMedium,
                color = Color.White,
                fontWeight = FontWeight.Bold
            )
            
            Text(
                text = "Join NoorGuard Family",
                style = MaterialTheme.typography.bodyLarge,
                color = Color.White.copy(alpha = 0.8f)
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Register Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surface
                ),
                elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(24.dp)
                ) {
                    // First Name
                    OutlinedTextField(
                        value = viewModel.firstName,
                        onValueChange = { viewModel.firstName = it },
                        label = { Text("First Name") },
                        leadingIcon = { Icon(Icons.Default.Person, null) },
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                        singleLine = true
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // Last Name
                    OutlinedTextField(
                        value = viewModel.lastName,
                        onValueChange = { viewModel.lastName = it },
                        label = { Text("Last Name") },
                        leadingIcon = { Icon(Icons.Default.Person, null) },
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                        singleLine = true
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // Email
                    OutlinedTextField(
                        value = viewModel.email,
                        onValueChange = { viewModel.email = it },
                        label = { Text("Email") },
                        leadingIcon = { Icon(Icons.Default.Email, null) },
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(
                            keyboardType = KeyboardType.Email,
                            imeAction = ImeAction.Next
                        ),
                        singleLine = true
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // Password
                    OutlinedTextField(
                        value = viewModel.password,
                        onValueChange = { viewModel.password = it },
                        label = { Text("Password") },
                        leadingIcon = { Icon(Icons.Default.Lock, null) },
                        trailingIcon = {
                            IconButton(onClick = { passwordVisible = !passwordVisible }) {
                                Icon(
                                    if (passwordVisible) Icons.Default.VisibilityOff
                                    else Icons.Default.Visibility,
                                    contentDescription = null
                                )
                            }
                        },
                        visualTransformation = if (passwordVisible) VisualTransformation.None
                        else PasswordVisualTransformation(),
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(
                            keyboardType = KeyboardType.Password,
                            imeAction = ImeAction.Next
                        ),
                        singleLine = true
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // Confirm Password
                    OutlinedTextField(
                        value = viewModel.confirmPassword,
                        onValueChange = { viewModel.confirmPassword = it },
                        label = { Text("Confirm Password") },
                        leadingIcon = { Icon(Icons.Default.Lock, null) },
                        trailingIcon = {
                            IconButton(onClick = { confirmPasswordVisible = !confirmPasswordVisible }) {
                                Icon(
                                    if (confirmPasswordVisible) Icons.Default.VisibilityOff
                                    else Icons.Default.Visibility,
                                    contentDescription = null
                                )
                            }
                        },
                        visualTransformation = if (confirmPasswordVisible) VisualTransformation.None
                        else PasswordVisualTransformation(),
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(
                            keyboardType = KeyboardType.Password,
                            imeAction = ImeAction.Done
                        ),
                        keyboardActions = KeyboardActions(
                            onDone = {
                                focusManager.clearFocus()
                                viewModel.register(onRegisterSuccess)
                            }
                        ),
                        singleLine = true
                    )
                    
                    // Error Message
                    if (viewModel.errorMessage != null) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = viewModel.errorMessage!!,
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    // Register Button
                    Button(
                        onClick = { viewModel.register(onRegisterSuccess) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(50.dp),
                        enabled = !viewModel.isLoading &&
                                viewModel.firstName.isNotEmpty() &&
                                viewModel.email.isNotEmpty() &&
                                viewModel.password.isNotEmpty() &&
                                viewModel.confirmPassword.isNotEmpty(),
                        colors = ButtonDefaults.buttonColors(containerColor = EmeraldGreen)
                    ) {
                        if (viewModel.isLoading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(24.dp),
                                color = Color.White
                            )
                        } else {
                            Text("Register", style = MaterialTheme.typography.titleMedium)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    TextButton(onClick = onNavigateToLogin) {
                        Text(
                            text = "Already have an account? Login",
                            color = EmeraldGreen
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}
