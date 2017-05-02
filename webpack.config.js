// module.exports = {
//   entry: ['whatwg-fetch', __dirname + '/appjs/index.js'],
//   output: {
//     path: __dirname + '/shared/static/shared/js/',
//     filename: 'app.js'
//   },
//   module: {
//     rules: [
//       {
//         test: /\.js$/,
//         exclude: /node_modules/,
//         use: {
//           loader: 'babel-loader',
//           options: {
//             presets: ['es2015', 'stage-0'],
//             plugins: [
//             ["transform-react-jsx", { "pragma": "h" }]
//             ]
//           }
//         },
//       }
//     ]
//   }
// };
