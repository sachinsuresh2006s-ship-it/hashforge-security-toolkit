const API = "http://127.0.0.1:8000";


// Generate / Encode
async function generateHash(){

    const text = document.getElementById("inputText").value.trim();
    const algo = document.getElementById("algorithm").value;
    const resultBox = document.getElementById("result");

    if(!text){
        resultBox.innerText = "Please enter text";
        return;
    }

    let url = "";

    if(["md5","sha1","sha256","sha512"].includes(algo)){
        url = `${API}/hash/${algo}`;
    }

    else if(algo === "base64_encode"){
        url = `${API}/encode/base64`;
    }

    else if(algo === "base64_decode"){
        url = `${API}/decode/base64`;
    }

    else if(algo === "hex_encode"){
        url = `${API}/encode/hex`;
    }

    else if(algo === "hex_decode"){
        url = `${API}/decode/hex`;
    }

    try{

        const response = await fetch(url,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({text:text})
        });

        const data = await response.json();

        resultBox.innerText = data.hash || data.result;

    }catch(error){

        resultBox.innerText = "API connection failed";

    }
}


// Crack Hash (manual algorithm)
async function crackHash(){

    const hash = document.getElementById("inputText").value.trim();
    const algo = document.getElementById("algorithm").value;
    const resultBox = document.getElementById("result");

    if(!hash){
        resultBox.innerText = "Enter hash first";
        return;
    }

    try{

        const response = await fetch(`${API}/crack`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                hash:hash,
                algorithm:algo
            })
        });

        const data = await response.json();

        resultBox.innerText = `Password: ${data.password}`;

    }catch(error){

        resultBox.innerText = "Crack request failed";

    }
}


// Auto Detect + Crack
async function autoCrack(){

    const hash = document.getElementById("inputText").value.trim();
    const resultBox = document.getElementById("result");

    if(!hash){
        resultBox.innerText = "Enter hash first";
        return;
    }

    try{

        const response = await fetch(`${API}/auto-crack`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                hash:hash
            })
        });

        const data = await response.json();

        resultBox.innerText =
`Algorithm: ${data.algorithm}
Password: ${data.password}`;

    }catch(error){

        resultBox.innerText = "Auto crack failed";

    }
}


// File Hashing
async function hashFile(){

    const fileInput = document.getElementById("fileInput");
    const resultBox = document.getElementById("fileResult");

    if(fileInput.files.length === 0){
        resultBox.innerText = "Please select a file";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try{

        const response = await fetch(`${API}/filehash`,{
            method:"POST",
            body:formData
        });

        const data = await response.json();

        resultBox.innerText =
`MD5: ${data.md5}
SHA1: ${data.sha1}
SHA256: ${data.sha256}
SHA512: ${data.sha512}`;

    }catch(error){

        resultBox.innerText = "File hashing failed";

    }
}