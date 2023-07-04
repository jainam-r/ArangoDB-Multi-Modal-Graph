

export default function Mongo(){
    const { MongoClient, ServerApiVersion } = require('mongodb');
    const pwd = 'zenteiq'
    const uri = "mongodb+srv://jainam-r:"+pwd+"@cluster0.ntxqi3q.mongodb.net/?retryWrites=true&w=majority1";
    // Create a MongoClient with a MongoClientOptions object to set the Stable API version
    const client = new MongoClient(uri, {
    serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
    }
    });
    async function run(){
        try{
            await client.connect();
            await client.db("admin").command({ping: 1})
            console.log("Connected successfully")
        }
        finally{
            await client.close()
        }
        // await client.close();
    }
    run().catch(console.dir)
    return (
        <div>
            <h2>Jainam</h2>
        </div>
    )
}