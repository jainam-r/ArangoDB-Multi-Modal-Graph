import {useState,useEffect} from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import { Typography } from '@mui/material';

export default function Home(){
    const [data, setData] = useState(null);
    // const sk = document.getElementById("outlined-basic");
    const [sk,setsk] = useState('')

    async function fetchData(){
        const sk2 = document.getElementById("outlined-basic").value
        console.log(sk2)
        let data1 = '{"username":"root","password":""}';
        
        let data =  `{"query" :"FOR course in courses FOR x in course.concepts_content FILTER x==@skill RETURN course", "count" : true, "bindVars" :{"skill":"Python"}}`;
        
        try{
            const res1 = await axios.post('http://localhost:8529/_open/auth',data1,{
                headers: { 
                    'Content-Type': 'text/plain'
                }
            })
            const token = res1.data['jwt']
            console.log(token)
            const res2 = await axios.post('http://localhost:8529/_db/Course/_api/cursor',data,{
                headers: { 
                    'Content-Type': 'text/plain', 
                    'Authorization': 'Bearer '+token
                }  
            })
            console.log(res2.data['result'])
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
    const Course=({name, domain, duration, price, description}) => {
        return (
            <div>
            <div class="box box1">
           
           <h3>{name}</h3>
           {/* <input type="text" id="skills" value="Course skills"/> */}
           <input type="text" id="domain" value="{domain}"/>
           <input type="text" id="price" value="Course price"/>
           <input type="text" id="duration" value="Course duration"/>
           <input type="text" id="type" value="Course type"/>
           <input type="text" id="content" value="Course content"/>
       </div>
            <Card sx={{maxWidth:350}}>
                <CardHeader title={name} subheader={domain}></CardHeader>
                <CardContent>
                    <Typography variant='body2' color="text.secondary">
                        {description}
                    </Typography>
                </CardContent>
                <br/>
                <br/>
            </Card>
            </div>
        )
    }

return(
    <div>
    <div class="topnav">
        <img src="logo.png" alt="Logo" class="logok" />
        <h1 class="head">Zenteiq</h1>
        <div class="search-container">
        <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <TextField id="outlined-basic" label="Search any career or skill" variant="outlined" value={sk} onChange={e=>setsk(e.target.value)}/>
      <Button variant="contained" type="submit" onClick={fetchData}>Search</Button>
      
    </Box>
        </div>
    </div>
    
    <Box sx={{flexDirection:'column'}}>
        {data && data.map((dat)=>(
            <Course key={dat._key} 
            name={dat.Course_name} 
            domain={dat.course_domain} 
            duration={dat.course_duration}
            price={dat.course_price}
            description={dat.description}/>
        ))}
    </Box>
    </div>
)
}