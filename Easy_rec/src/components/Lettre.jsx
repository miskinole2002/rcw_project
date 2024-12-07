import React,{useContext} from "react";
import Api from "../contexts/request";
import* as yup from"yup"
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

const Lettre=()=>{
const{SOURCE}=useContext(Api) 

const formSchema = yup.object({
    email: yup.string().required("le champs est requis"),
  });
  
  const {
    handleSubmit,
    register,
    formState: { errors },
  } = useForm({ resolver: yupResolver(formSchema) });
  
  const submit = async (values) => {
  const offre_id=values.email
  const response= await fetch(`${SOURCE}/get_lettre_motivation/${offre_id}`, {
  
  method:"Get",
  
  headers:{"Content-Type":"application/json"},

  
  });
  const data= await response.json()
  console.log('reponse:',data)
  };

return(
    <>
    <form action="" onSubmit={handleSubmit(submit)}>
        
        <div>
          <label htmlFor="email">id</label>
        <input type="text" id="email" {...register("email")} />
        </div>

       
        <button type="submit">connection</button>
        
      </form>
    </>
)
}

export default Lettre