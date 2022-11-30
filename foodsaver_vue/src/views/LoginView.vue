<template>
	<div class="page-log-in">
		<div class="columns">
			<div class="column is-4 is-offset-4">
				<h1 class="title">Log in</h1>

				<form @submit.prevent="submitForm">
					<div class="field">
						<label>Username</label>
						<div class="control">
							<input type="text" class="input" v-model="username" />
						</div>
					</div>

					<div class="field">
						<label>Password</label>
						<div class="control">
							<input type="password" class="input" v-model="password" />
						</div>
					</div>

					<div class="notification is-danger" v-if="errors.length">
						<p v-for="error in errors" v-bind:key="error">{{ error }}</p>
					</div>

					<div class="field">
						<div class="control">
							<button class="button is-primary">Log in</button>
						</div>
					</div>

					<hr />

					Or <router-link to="/sign-up">click here</router-link> to sign up!
				</form>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
	name: 'LogIn',
	data() {
		return {
			username: '',
			password: '',
			errors: []
		}
	},
	mounted() {
		document.title = 'Log In | Food Saver'
	},
	methods: {
		async submitForm() {
			// Reset previous authentication
			axios.defaults.headers.common['Authorization'] = ''
			localStorage.removeItem('token')
			localStorage.removeItem('user')

			const formData = {
				username: this.username,
				password: this.password
			}
			await axios
				.post('/api/v1/token/login/', formData)
				.then((response) => {
					const token = response.data.auth_token
					const username = this.username
					this.$store.commit('setToken', token)
					this.$store.commit('setCurrentUser', username)

					axios.defaults.headers.common['Authorization'] = 'Token ' + token
					// store token in localstorage to make token persists once refresh
					localStorage.setItem('token', token)
					localStorage.setItem('username', username)

					toast({
						message: 'Welcome back Vendor!',
						type: 'is-success',
						dismissible: true,
						pauseOnHover: true,
						duration: 2000,
						position: 'bottom-right'
					})
					this.$router.push('/vendor-dashboard')
				})
				.catch((error) => {
					if (error.response) {
						for (const property in error.response.data) {
							this.errors.push(`${property}: ${error.response.data[property]}`)
						}
					} else {
						this.errors.push('Something went wrong. Please try again')

						console.log(JSON.stringify(error))
					}
				})
		}
	}
}
</script>
