import { Get } from "./Get";

function App() {
  const { Database, aql } = require("arangojs");

  const db = new Database({
    url: "http://127.0.0.1:8529",
    databaseName: "test1",
    auth: { username: "root", password: "" },
  });
  var final_item = db.collection('final_item');
  console.log(db)
  const getCollection = async(name) => {
    return await db.collection(name)
  }
  const q1 = async(name)=>{
    var cc;
    await getCollection('final_item')
    const results = await db.query(aql`
    FOR item in ${final_item} 
    RETURN item._key
    `).then(
      cursor => cursor.all()
    ).then(
      keys => console.log(keys.join(', ')),
      err => console.error('Failed to execute ',err)
    );
    for await (cc of results){
      console.log(cc)
    }
    return cc;
  }
  q1()

  // const ct = async() =>{
  //   const ct = await Get()
  //   console.log(ct)
  // }
  // ct();


  return (
    <div className="App">
      <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
