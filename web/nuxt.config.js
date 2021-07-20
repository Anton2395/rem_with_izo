export default {

    target: 'static',
    server:{
        host: '0.0.0.0',
        port: 80

    },

    mode: 'spa',
    /*
     ** Headers of the page
     */
    head: {
        title: process.env.npm_package_name || '',
        meta: [{
            charset: 'utf-8'
        },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1'
            },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || ''
            }
        ],
        link: [{
            rel: 'icon',
            type: 'image/png',
            href: './favicon.png'
        }]
    },
    /*
     ** Customize the progress-bar color
     */
    loading: {
        color: '#597CC7'
    },
    /*
     ** Global CSS
     */
    css: [
        'normalize.css',
        '~/assets/css/global-styles.css'
    ],
    /*
     ** Plugins to load before mounting the App
     */
    plugins: [{
        src: "~/plugins/highcharts.js",
        ssr: true
    },

        {
            src: "~/plugins/iconify.js",
            ssr: true
        },
        {
            src: "~/plugins/element-ui",
            ssr: true
        },


    ],
    /*
     ** Nuxt.js dev-modules
     */
    buildModules: [],
    /*
     ** Nuxt.js modules
     */
    modules: [
        '@nuxtjs/axios',
        '@nuxtjs/auth',
        'nuxt-webfontloader',
    ],
    // elementUI: {
    //     components: ['TimeSelect'],
    //     locale: 'ru',
    // },
    axios: {
        // baseURL: 'http://192.168.0.6:8000/',
        // baseURL: 'http://172.20.10.2:8001',
        // baseURL: 'http://128.65.54.166:8082',

        // baseURL:  'http://localhost:50001/',
        baseUrl: 'http://itech.by:50002/',

        proxy: false,
    },
    router: {
        middleware: ['auth'],
    },
    auth: {
        localStorage: false,
        cookie: {
            options: {
                expires: 7,
            }
        },
        strategies: {
            local: {

                endpoints: {
                    login: {url: '/user/login/', method: 'post', propertyName: 'token'},
                    logout: {url: '/user/logout/', method: 'post'},
                    user: {url: '/user/myname/', method: 'get', propertyName:null}
                },
                tokenRequired: true,
                // tokenType: 'bearer',
                tokenType: 'Token',
                globalToken: true,
                autoFetchUser: true
            },
            user: {
                property: '',
               // autoFetch: true
              },
        },
        redirect: {
            login: '/login',
            logout: '/login',
            callback: '/login',
            home: false,
        },
        plugins: ['~/plugins/auth.js']
    },
    proxy: {
        // '/user/': 'http://185.231.71.153:8000',
        // '/api/Users/': 'http://185.231.71.153:8000',
        // '/api/': 'http://185.231.71.153:8000',
    },

    webfontloader: {
        events: false,
        google: {
            families: ['Montserrat:400,500,600:cyrillic&display=swap']
        },
        timeout: 5000
    },
    /*
     ** Build configuration
     */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {
        }
    },
    generate: {
        dir: 'dist'
    }
}
