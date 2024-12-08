import React,{useContext} from "react";
import Api from "../contexts/request";
import* as yup from"yup"
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

const Chat=()=>{
const{SOURCE}=useContext(Api) 

const formSchema = yup.object({
    id: yup.string().required("le champs est requis"),
    text: yup.string().required("le champs est requis"),
  });
  
  const {
    handleSubmit,
    register,
    formState: { errors },
  } = useForm({ resolver: yupResolver(formSchema) });
  
  const submit = async (values) => {
  console.log(values);
  const response= await fetch(`${SOURCE}/chatbot`, {
  
  method:"POST",
  
  headers:{"Content-Type":"application/json"},
  
  body:JSON.stringify(values),
  });
  const data= await response.json()
  console.log('reponse:',data)
  };

return(
    <>
    <form action="" onSubmit={handleSubmit(submit)}>
        
        <div>
          <label htmlFor="id">id </label>
        <input type="text" id="id" {...register("id")} />
        </div>

        <div>
          <label htmlFor="text"> question </label>
        <input type="text" id="text" {...register("text")} />
        </div>
      
        <button type="submit">connection</button>
        
      </form>
    </>
)
}

export default Chat