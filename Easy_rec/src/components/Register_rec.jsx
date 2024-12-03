import React,{useContext} from "react";
import Api from "../contexts/request";
import* as yup from"yup"
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";


const Register_rec=()=>{
const{SOURCE}=useContext(Api) 


const formSchema = yup.object({
  nom_entreprise:yup.string().required("le champs est obligatoire"),
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
const response= await fetch(`${SOURCE}/register_recruteur`, {

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
   
          <label htmlFor="nom_entreprise"> nom de l'entreprise</label>
          <input type="text" name="nom_entreprise" id="nom_entreprise" {...register("nom_entreprise")} />
        </div>

        <div>
          <label htmlFor="email">adresse email</label>
        <input type="text" id="email" {...register("email")} />
        </div>

        <div>
          <label htmlFor="password">mot de passe</label>
        <input type="text" id="password" {...register("password")} />
        </div>
      
        <button type="submit">s'incrire</button>
        
      </form>
    </>
)
}
export default Register_rec