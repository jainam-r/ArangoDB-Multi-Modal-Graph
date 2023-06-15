import {useState,useEffect} from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

export default function Home(){
    const [data, setData] = useState(null);
    async function fetchData(){
        let data1 = '{"username":"root","password":""}';
        let data = '{ "query" : "FOR u IN final_item LIMIT 5 RETURN u", "count" : true, "batchSize" : 2 }';
        
        try{
            const res1 = await axios.post('http://localhost:8529/_open/auth',data1,{
                headers: { 
                    'Content-Type': 'text/plain'
                }
            })
            const token = res1.data['jwt']
            console.log(token)
            const res2 = await axios.post('http://localhost:8529/_db/test1/_api/cursor',data,{
                headers: { 
                    'Content-Type': 'text/plain', 
                    'Authorization': 'Bearer '+token
                }  
            })
            console.log(res2.data['result'][0])
            console.log('here')
            setData(res2.data['result'])
        }
        catch(error){
            console.log(error)
        }
        // e.preventDefault()
    }
    useEffect(()=>{
        fetchData()
    },[setData])

return(
    <div>
    <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
      onSubmit={fetchData}
    >
      <TextField id="outlined-basic" label="Outlined" variant="outlined" />
      <Button variant="contained" type="submit">Contained</Button>
      <TextField id="outlined-basic" label="Outlined" variant="outlined" />
      
    </Box>
    <div>
        {data && data.map((dat)=>(
            <p key={dat._key}>{dat._key}</p>
        ))}
    </div>
    </div>
)
}