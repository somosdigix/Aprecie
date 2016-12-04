import eslint from 'rollup-plugin-eslint';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import string from 'rollup-plugin-string';

import postcss from 'rollup-plugin-postcss';
import simplevars from 'postcss-simple-vars';
import nested from 'postcss-nested';
import cssnext from 'postcss-cssnext';
import cssnano from 'cssnano';

export default {
  entry: './app.js',
  dest: './dist/app.dist.js',
  format: 'iife',
  sourceMap: 'inline',
  plugins: [
    postcss({
      plugins: [
        simplevars(),
        nested(),
        cssnext({ warnForDuplicates: false }),
        cssnano()
      ],
      extensions: [ '.css' ]
    }),

    resolve({
      jsnext: true,
      main: true,
      browser: true
    }),

    commonjs(),

    eslint({
      exclude: [
        './styles/*.css',
        './**/*.html'
      ]
    }),

    string({
      include: '**/*.html',
      exclude: ['**/index.html']
    })
  ]
};
