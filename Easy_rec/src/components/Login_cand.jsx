import React,{useContext} from "react";
import Api from "../contexts/request";
import* as yup from"yup"
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

const Login_cand=()=>{
const{SOURCE}=useContext(Api) 

const formSchema = yup.object({
    email: yup.string().required("le champs est requis"),
    password: yup.string().required("le champs est requis"),
  });
  
  const {
    handleSubmit,
    register,
    formState: { errors },
  } = useForm({ resolver: yupResolver(formSchema) });
  
  const submit = async (values) => {
  console.log(values);
  const response= await fetch(`${SOURCE}/log_candidat`, {
  
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
          <label htmlFor="email">adresse email</label>
        <input type="text" id="email" {...register("email")} />
        </div>

        <div>
          <label htmlFor="password">mot de passe</label>
        <input type="text" id="password" {...register("password")} />
        </div>
      
        <button type="submit">connection</button>
        
      </form>
    </>
)
}

export default Login_cand