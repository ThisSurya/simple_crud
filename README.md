### In be_simple_crud
1. change directory to be_simple_crud
`cd be_simple_crud`
2. activate environment
`conda activate <env>`
3. pip install
`pip install requirements.txt`
4. Init db first
`flask db init`
5. Make commit migration
`flask db migration -m "your comment" `
6. migrate db
`flask db upgrade`
7. run flask

### In simple_crud
1. change directory to simple_crud
`cd simple_crud`
2. run npm install to install dependencies
`npm install` or `yarn install` or whatever based on your package manager
3. run dev
`npm run dev`