# Terraform infrastructure on Azure

## Explanation
The following Terraform project deploys the required infrastructure to run my web application and database. This includes:
1. 2 VMs to run 2 instances of my app
2. A VM to run the PostgreSQL DB
3. A Load Balancer that connects to the web VMs
4. A "Network Security Group" with rules to enforce proper access to each VM.


### Installation  
To install the infrastructure, run the following commands in a terminal:  
    
```
git clone https://github.com/LiorAtari/Terraform_project.git

cd Terraform_project

terraform init

terraform plan -out <name for the plan>

terraform apply <name of the plan created>
```

![architecture](map.png)


