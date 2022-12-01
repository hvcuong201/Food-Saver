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
					<form @submit.prevent="createProduct">
						<div class="field">
							<label class="label">Product's name</label>
							<div class="control">
								<input type="text" class="input" v-model="product_name" />
							</div>
						</div>

						<div class="field">
							<label class="label">Category</label>
							<div class="control">
								<div class="select">
									<select v-model="product_category">
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
								<input v-model="product_price" type="number" class="input" min="0.00" max="1000.00" step="any" />
							</div>
						</div>

						<div class="field">
							<label class="label">Quantity</label>
							<div class="control">
								<input v-model="product_qty" type="number" class="input" min="1" />
							</div>
						</div>

						<div class="field">
							<label class="label">Unit</label>
							<div class="control">
								<input v-model="product_unit" type="text" class="input" />
							</div>
						</div>

						<div class="field">
							<label class="label">Description</label>
							<div class="control">
								<textarea v-model="product_desc" class="textarea" placeholder="Textarea"></textarea>
							</div>
						</div>

						<div class="field">
							<label class="label">Product's image</label>
							<div class="file">
								<div class="control">
									<input class="file my-4" type="file" name="image" @change="onFileSelected" />
								</div>
							</div>
						</div>

						<div class="field">
							<div class="control">
								<button class="button is-primary">Publish</button>
							</div>
						</div>
					</form>
				</div>
			</div>

			<div class="column is-12">
				<div class="box">
					<h1 class="subtitle">Your on-sale products:</h1>
					<template v-if="productsByVendorID.length > 0">
						<div class="columns is-multiline">
							<div class="column is-3" v-for="product in productsByVendorID" v-bind:key="product.vendor">
								<div class="box">
									<figure class="image mb-4 is-3by2">
										<img :src="product.get_thumbnail" />
									</figure>
									<h3 class="is-size-4">{{ product.name }} ({{ product.quantity }} {{ product.unit }}s)</h3>
									<p class="is-size-4 has-text-grey">${{ product.price }} per {{ product.unit }}</p>

									<RouterLink v-bind:to="product.get_absolute_url" class="button is-info mt-4">View Details</RouterLink>
									<template v-if="$store.state.isAuthenticated">
										<button class="button is-danger mt-4 mx-2" @click="deleteProduct(product.id)">Delete</button>
									</template>
								</div>
							</div>
						</div>
					</template>
					<template v-else> <p class="is-primary">Start uploading your products...</p> </template>
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
import { toast } from 'bulma-toast'
export default {
	name: 'VendorDashboard',
	data() {
		return {
			username: '',
			vendorid: '',
			productsByVendorID: [],
			product_name: '',
			product_category: '',
			product_price: '',
			product_qty: '',
			product_unit: '',
			product_desc: '',
			errors: [],
			selectedFile: null
		}
	},
	mounted() {
		document.title = 'Dashboard | Food Saver'

		if (localStorage.username) {
			this.username = localStorage.getItem('username')
		}
		this.getVendorID()
		this.getProductsByVendorID()
	},
	methods: {
		async onFileSelected(event) {
			//this.selectedFile = event.target.files[0]
			const toBase64 = (file) =>
				new Promise((resolve, reject) => {
					const reader = new FileReader()
					reader.readAsDataURL(file)
					reader.onload = () => resolve(reader.result)
					reader.onerror = (error) => reject(error)
				})
			this.selectedFile = await toBase64(event.target.files[0])
			console.log(this.selectedFile)
		},
		async getVendorID() {
			await axios
				.get('/api/v1/products/vendor/')
				.then((response) => {
					this.vendorid = response.data
				})
				.catch((error) => {
					console.log(error)
				})
		},
		async getProductsByVendorID() {
			this.$store.commit('setIsLoading', true)

			await axios
				.get('/api/v1/products/by-vendor/')
				.then((response) => {
					this.productsByVendorID = response.data
				})
				.catch((error) => {
					console.log(error)
				})

			this.$store.commit('setIsLoading', false)
		},
		async createProduct() {
			this.errors = []
			if (this.product_name === '') {
				this.errors.push('The product name field is missing!')
			}
			if (this.product_category === '') {
				this.errors.push('The product_category field is missing!')
			}
			if (this.product_price === '') {
				this.errors.push('The product price field is missing!')
			}
			if (this.product_qty === '') {
				this.errors.push('The product quantity field is missing!')
			}
			if (this.product_unit === '') {
				this.errors.push('The product unit field is missing!')
			}
			if (!this.errors.length) {
				this.$store.commit('setIsLoading', true)

				if (this.product_category == 'Dairy') {
					this.product_category = 2
				} else if (this.product_category == 'Fruits') {
					this.product_category = 3
				} else if (this.product_category == 'Protein') {
					this.product_category = 1
				} else if (this.product_category == 'Vegetables') {
					this.product_category = 4
				}
				const slugify = (str) =>
					str
						.toLowerCase()
						.trim()
						.replace(/[^\w\s-]/g, '')
						.replace(/[\s_-]+/g, '-')
						.replace(/^-+|-+$/g, '')

				const data = {
					name: this.product_name,
					category: this.product_category,
					price: this.product_price,
					quantity: this.product_qty,
					unit: this.product_unit,
					description: this.product_desc,
					vendor: this.vendorid,
					slug: slugify(this.product_name),
					base64_img: this.selectedFile
				}

				this.$store.commit('setIsLoading', true)

				await axios
					.post('/api/v1/products/vendor/', data)
					.then((response) => {
						console.log(response.data)
						toast({
							message: 'Publish Product Successfully.',
							type: 'is-success',
							dismissible: true,
							pauseOnHover: true,
							duration: 2000,
							position: 'bottom-right'
						})
					})
					.catch((error) => {
						toast({
							message: 'Publish Product Unsuccessfully.',
							type: 'is-danger',
							dismissible: true,
							pauseOnHover: true,
							duration: 2000,
							position: 'bottom-right'
						})
						console.log(error)
					})

				this.getProductsByVendorID()
				this.$store.commit('setIsLoading', false)
			} else {
				this.errors.forEach((error) => {
					toast({
						message: JSON.stringify(error),
						type: 'is-danger',
						dismissible: true,
						pauseOnHover: true,
						duration: 2000,
						position: 'bottom-right'
					})
				})
			}
		},
		async deleteProduct(id) {
			console.log(id)
			this.$store.commit('setIsLoading', true)

			await axios
				.delete('/api/v1/products/vendor/', { data: { pk: id } })
				.then((response) => {
					console.log(response.data)
					toast({
						message: 'Delete Product Successfully.',
						type: 'is-success',
						dismissible: true,
						pauseOnHover: true,
						duration: 2000,
						position: 'bottom-right'
					})
				})
				.catch((error) => {
					console.log(error)
					console.log(response.data)
					toast({
						message: 'Delete Product Unsuccessfully.',
						type: 'is-dangerr',
						dismissible: true,
						pauseOnHover: true,
						duration: 2000,
						position: 'bottom-right'
					})
				})
			this.getProductsByVendorID()
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
