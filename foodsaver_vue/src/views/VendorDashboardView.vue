<template>
	<div class="page-my-account">
		<div class="columns is-multiline is-centered">
			<div class="column is-12 mb-5">
				<h1 class="title is-pulled-left">
					Hello, <span class="has-text-info-dark">{{ getName() }}</span>
				</h1>
				<button @click="logout()" class="button is-danger is-pulled-right">Log out</button>
			</div>

			<div class="column is-8">
				<div class="box">
					<h1 class="subtitle">Create a new Product for sale</h1>
					<form>
						<div class="field">
							<label class="label">Product's name</label>
							<div class="control">
								<input type="text" class="input" />
							</div>
						</div>

						<div class="field">
							<label class="label">Category</label>
							<div class="control">
								<div class="select">
									<select>
										<option>Dairy</option>
										<option>Fruits</option>
										<option>Protein</option>
										<option>Vegetables</option>
									</select>
								</div>
							</div>
						</div>

						<div class="field">
							<label class="label">Price</label>
							<div class="control">
								<input type="number" class="input" min="0.01" max="1000.00" step="0.1" />
							</div>
						</div>

						<div class="field">
							<label class="label">Quantity</label>
							<div class="control">
								<input type="number" class="input" min="1" />
							</div>
						</div>

						<div class="field">
							<label class="label">Unit</label>
							<div class="control">
								<input type="text" class="input" />
							</div>
						</div>

						<div class="field">
							<label class="label">Description</label>
							<div class="control">
								<textarea class="textarea" placeholder="Textarea"></textarea>
							</div>
						</div>

						<div class="field">
							<label class="label">Product's image</label>
							<div class="file">
								<div class="control">
									<label class="file-label">
										<input class="file-input" type="file" name="image" />
										<span class="file-cta">
											<span class="file-icon">
												<i class="fas fa-upload"></i>
											</span>
											<span class="file-label"> Choose a file… </span>
										</span>
									</label>
								</div>
							</div>
						</div>

						<div class="field is-grouped">
							<div class="control">
								<button class="button is-primary">Publish</button>
							</div>
							<div class="control">
								<button class="button is-link is-light">Cancel</button>
							</div>
						</div>
					</form>
				</div>
			</div>

			<div class="column is-12">
				<div class="box">
					<h1 class="subtitle">Your on-sale products:</h1>
					<div class="columns is-multiline">
						<div class="column is-3" v-for="product in productsByVendorID" v-bind:key="product.vendor">
							<div class="box">
								<figure class="image mb-4 is-3by2">
									<img :src="product.get_thumbnail" />
								</figure>
								<h3 class="is-size-4">{{ product.name }} ({{ product.quantity }} {{ product.unit }}s)</h3>
								<p class="is-size-4 has-text-grey">${{ product.price }} per {{ product.unit }}</p>

								<RouterLink v-bind:to="product.get_absolute_url" class="button is-info mt-4">View Details</RouterLink>
								<button class="button is-danger mt-4 mx-2">Delete</button>
							</div>
						</div>
					</div>
				</div>

				<div class="box">
					<h1 class="subtitle">Your order</h1>
				</div>
			</div>

			<hr />
		</div>
	</div>
</template>

<script>
import axios from 'axios'

export default {
	name: 'VendorDashboard',
	data() {
		return {
			username: '',
			vendorid: '',
			productsByVendorID: []
		}
	},
	mounted() {
		document.title = 'VendorDashboard | Food Saver'

		if (localStorage.username) {
			this.username = localStorage.getItem('username')
		}

		this.getProductsByVendorID()
	},
	methods: {
		async getProductsByVendorID() {
			this.$store.commit('setIsLoading', true)

			await axios
				.get('/api/v1/products/by-vendor/', { vendorid: 2 })
				.then((response) => {
					this.productsByVendorID = response.data
				})
				.catch((error) => {
					console.log(error)
				})

			this.$store.commit('setIsLoading', false)
		},
		getName() {
			return this.username
		},
		logout() {
			axios.defaults.headers.common['Authorization'] = ''
			localStorage.removeItem('token')
			localStorage.removeItem('username')
			localStorage.removeItem('userid')
			this.$store.commit('removeToken')
			this.$router.push('/')
		}
	}
}
</script>
