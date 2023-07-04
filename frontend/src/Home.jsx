import {useState} from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import logo from '../src/zenteiq_logo.png'
import Grid from '@mui/material/Grid';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import SearchIcon from '@mui/icons-material/Search'; 


export default function Home(){
    const [data, setData] = useState('');
    const [sk,setsk] = useState('')

    async function fetchData(){
        console.log(sk)
        let data1 = '{"username":"root","password":""}';
        
        let data2 =  `{"query" :"FOR course in courses FOR x in course.concepts_content FILTER x==@skill RETURN course", "count" : true, "bindVars" :{"skill":"${sk}"}}`;
        
        try{
            const res1 = await axios.post('http://localhost:8529/_open/auth',data1,{
                headers: { 
                    'Content-Type': 'text/plain'
                }
            })
            const token = res1.data['jwt']
            console.log(token)
            const res2 = await axios.post('http://localhost:8529/_db/Course/_api/cursor',data2,{
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
    }

    const Course=({name, domain, duration, price, description,concepts}) => {
        return (
            <div>
            <br/>
            <Grid item>
            <Card sx={{width:'100vh', display:'block'}}>
                <CardContent>
                    <Typography variant='h3' color="text.primary">
                        <b>{name}</b>
                    </Typography>
                    <Typography variant='subtitle1' color="text.secondary">
                        Description : {description}
                    </Typography>
                    <Typography>
                    Skills to learn : {concepts.map((con)=>(
                            <Typography sx={{display:'inline-block',verticalAlign:'middle'}} key={con}> {con}, </Typography>
                        ))}
                    </Typography>
                    <Typography>
                        Domain : {domain}
                    </Typography>
                    <Typography>
                        Duration : {duration}
                    </Typography>
                    <Typography>
                        Price : Rs {price}
                    </Typography>
                    
                </CardContent>
                <CardActions>
                    <Button size="small">Enroll</Button>
                </CardActions>
            </Card>
            </Grid>
            
            </div>
        )
    }
    const handleTextFieldChange = (e) =>{
        setsk(e.target.value)
    }
    const fetchData2 = (event) => {
        event.preventDefault()
        fetchData()
    }
return(
    <div>
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{backgroundColor:'white'}}>
        <Toolbar sx={{marginTop:2, marginBottom:2, justifyContent: "space-between"}}>
          <Box
            component="img"
            sx={{
            height: 64,
            }}
            alt="Your logo."
            src={logo}
        />
          {/* <Search sx={{outlineColor:'black'}}> */}
            {/* <StyledInputBase
              placeholder="Search any skill"
              inputProps={{ 'aria-label': 'search' }}
              value={sk}
              color="primary"
              onChange={handleTextFieldChange}
              
            /> */}
            <form>
            <Box sx={{alignItems:'end'}}>
            <TextField id="outlined-basic" 
            label="Search any skill" 
            variant="outlined" 
            value={sk} 
            onChange={handleTextFieldChange} 
            />
          <Button variant="contained" 
          type="submit" 
          onClick={fetchData2} 
          sx={{marginTop:1, marginLeft:1}}
         >
            <SearchIcon/>
          </Button>
          </Box>
          </form>
        </Toolbar>
      </AppBar>
    </Box>

    <Grid container
  spacing={0}
  direction="column"
  alignItems="center"
  justify="center"
  style={{ minHeight: '100vh' }}
 >
        {data && data.map((dat)=>(
            <Course key={dat._key} 
            name={dat.Course_Name} 
            domain={dat.course_domain} 
            duration={dat.course_duration}
            price={dat.course_price}
            description={dat.description}
            concepts={dat.concepts_content}
            />
        ))}
    </Grid>
    </div>
)
}