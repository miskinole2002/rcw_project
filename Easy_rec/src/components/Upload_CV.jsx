import React, { useState } from "react"
import { useContext } from "react";
import Api from "../contexts/request";

const Upload_cv=()=>{

const{SOURCE}=useContext(Api) 
const [file,setFile]=useState(null);

const handleFile=(e)=>{
    setFile(e.target.files[0])
}

const formData= new FormData()
formData.append("file",file)


const submit = async () => {
    console.log(file);
    const response= await fetch(`${SOURCE}/upload_cv`, {
    
    method:"POST",
    
    body:formData,
    });
     const data= await response.json()
     console.log('reponse:',data)
    };


return(

<div>
      <h1>Téléversez votre CV</h1>
      <input type="file" onChange={handleFile} />
      <button onClick={submit}>Téléverser</button>
      
</div>
)
}

export default Upload_cv