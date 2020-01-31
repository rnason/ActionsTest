<!-- VSCode Markdown Exclusions-->
<!-- markdownlint-disable MD025 Single Title Headers-->
# CloudMage Terraform ActionsTest Module


![Hero](images/tf_kms.png)

<br>

![Version-Badge](https://img.shields.io/badge/MODULE%20VERSION-v1.1.0-Green?style=for-the-badge&logo=terraform&logoColor=BLUE&logoWidth=25)

<br><br>

# Table of Contents

* [Getting Started](#getting-started)
* [Module Pre-Requisites and Dependencies](#module-pre-requisites-and-dependencies)
* [Module Directory Structure](#module-directory-structure)
* [Module Usage](#module-usage)
* [Terraform Variable Usage](#terraform-variables-usage)
  * [Inline Variable Declaration](#inline-variable-declaration)
  * [TFVar Variable Declaration](#tfvar-variable-declaration)
* [Required Module Variables](#required-variables)
  * :warning: kms_key_alias_name
  * :warning: kms_key_description
* [Optional Module Variables](#optional-module-variables)
  * :white_check_mark: kms_owner_principal_list
  * :white_check_mark: kms_admin_principal_list
  * :white_check_mark: kms_user_principal_list
  * :white_check_mark: kms_resource_principal_list
  * :white_check_mark: kms_tags
* [Module Example Usage](#module-example-usage)
* [Variables and TFVar Reference File Templates](#variables-and-tfvar-reference-file-templates)
* [Module Outputs Reference File Templates](#module-outputs-reference-file-templates)
* [Terraform Requirements](#terraform-requirements)
* [Recommended Terraform Utilities](#recommended-terraform-utilities)
* [Contacts and Contributions](#contacts-and-contributions)

<br><br>

# Getting Started

This Terraform module was created to quickly and easily provision a secure AWS Key Management Service (KMS) Customer Managed Key (CMK). CMK's are used for server-side encryption on AWS services such as S3 buckets, EBS volumes, Dynamo DB Tables, or any other service where data encryption is required. This module also includes optional variables that allow the consumer of the module to choose how KMS Key policies will be constructed and placed on be the CMK at the time of provisioning.

<br><br>

# Module Pre-Requisites and Dependencies

This module does not currently have any pre-requisites or dependency requirements.

<br><br>

# Module Directory Structure

```bash
.
├── outputs.tf
├── main.tf
├── requirements.txt
├── CHANGELOG.md
├── images
│   ├── tf_kms.png
│   ├── tf_kms_tags.png
│   ├── optional.png
│   ├── neon_optional.png
│   ├── required.png
│   └── neon_required.png
├── gendoc.py
├── example
│   ├── env.tfvars
│   ├── outputs.tf
│   ├── main.tf
│   ├── README.md
│   └── variables.tf
├── SampleGitHubCall.json
├── gendoc.log
├── TODO_NOTES.yaml
├── README.md
├── README.yaml
├── variables.tf
├── templates
│   ├── CHANGELOG.j2
│   └── README.j2
└── ORIGIN_README.md

```

<br><br>

# Module Usage

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket


    // Optional Variables with module defined default values assigned
    # kms_owner_principal_list    = []
    # kms_admin_principal_list    = []
    # kms_user_principal_list     = []
    # kms_resource_principal_list = []

    # kms_tags = {
    #   Provisioned_By = "Terraform"
    #   Module_GitHub_URL = "https://github.com/CloudMage-TF/AWS-KMS-Module.git"
    # }
}
```

<br><br>

# Terraform Variable Usage

Module variables that need to either be defined or re-defined with a non-default value can easily be hardcoded inline directly within the module call block or from within the root project that is consuming the module. If using the second approach then the root project must have it's own custom variables defined within the projects `variables.tf` file with set default values or with the values provided from a separate environmental `terraform.tfvar` file. Examples of both approaches can be found below. Note that for the standards used within this documentation, all variables will mostly use the first approach for ease of readability.

<br><br>

> :atom: &nbsp;[__Tip:__](Tip) <br> There is also a third way to provide variable values using Terraform data sources. A data source is a unique type of code block used within a project that either instantiates or collects data that can be referenced throughout the project. A data source, for example,  can be declared to read the terraform state file and gather all of the available information from a previously deployed project stack. Any of the data contained within the data source can then be referenced to set the value of a project or module variable.

<br><br>

## Inline Variable Declaration

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket
}
```

<br><br>

## TFVar Variable Declaration

<br>

### :file_folder: variables.tf

```terraform
variable "kms_key_alias_name" {
    type        = string
    description = "The alias that will be assigned to the provisioned KMS CMK. This value will be appended to alias/ within the module automatically."
}
variable "kms_key_description" {
    type        = string
    description = "The description that will be applied to the provisioned KMS Key."
}
```

<br>

### :file_folder: terraform.tfvars

```terraform
kms_key_alias_name  = prod/s3
kms_key_description = KMS key provisioned to encrypt prod s3 bucket
```

<br>

### :file_folder: main.tf

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = var.kms_key_alias_name
    kms_key_description = var.kms_key_description
}
```

<br><br>

# Required Variables

The following required module variables do not contain default values and must be set by the consumer of the module to use the module successfully.

<br>

## :warning: kms_key_alias_name


<br>

![Required](images/neon_required.png)

<br>

This variable should be passed containing the desired key alias that will be assigned to the provisioned KMS CMK.


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> The required `alias/` prefix is already defined in the module and not required as part of the variable string.


<br><br>

### :file_folder: Declaration of kms_key_alias_name within the modules variables.tf file

```terraform
variable "kms_key_alias_name" {
    type        = string
    description = "The alias that will be assigned to the provisioned KMS CMK. This value will be appended to alias/ within the module automatically."
}
```




<br><br>

### :file_folder: Setting the kms_key_alias_name module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
}
```




<br><br><br>

## :warning: kms_key_description


<br>

![Required](images/neon_required.png)

<br>

This variable should be passed containing a short description of what the provisioned KMS CMK will be used for as its value.



<br><br>

### :file_folder: Declaration of kms_key_description within the modules variables.tf file

```terraform
variable "kms_key_description" {
    type        = string
    description = "The description that will be applied to the provisioned KMS Key."
}
```




<br><br>

### :file_folder: Setting the kms_key_description module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket
}
```




<br><br><br>

# Optional Module Variables

The following optional module variables are not required because they already have default values assigned when the variables where defined within the modules `variables.tf` file. If the default values do not need to be changed by the root project consuming the module, then they do not even need to be included in the root project. If any of the variables do need to be changed, then they can be added to the root project in the same way that the required variables were defined and utilized. Optional variables also may alter how the module provisions resources in the cases of encryption or IAM policy generation. A variable could flag an encryption requirement when provisioning an S3 bucket or Dynamo table by providing a KMS CMK, for example. Another use case may be the passage of ARN values to allow users or roles access to services or resources, whereas by default permissions would be more restrictive or only assigned to the account root or a single IAM role. A detailed explanation of each of these optional variables can be found below:

<br><br>

## :white_check_mark: kms_owner_principal_list


<br>

![Optional](images/neon_optional.png)

<br>

This variable is used to define a list of users/roles that will be added to the KMS Key Owner policy statement. If the variable is not defined, then the key owner policy will be included to contain the account root user, allowing IAM the ability to assign key permissions using standard IAM policies. If a list of roles/users is defined, then the provided list will instead be used to determine the key owner principals. Typically this variable will only be used if the CMK will be shared, and the key provisioner needs to make another AWS account a key owner to allow IAM policies in the other account to define permission for the provisioned shared key. Image:


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> The key owner policy statement determines what users/roles own the provisioned KMS key. Owners have `kms:*` permissions on the CMK. They can perform any action on the key including performing any modifications to the key and the key policy.


<br><br>

### :file_folder: Declaration of kms_owner_principal_list within the modules variables.tf file

```terraform
variable "kms_owner_principal_list" {
    type        = list
    description = "List of users/roles/accounts that will own and have kms:* on the provisioned CMK."
    default     = []
}


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> You can not assign an IAM group as a policy principal, only IAM users/roles are allowed as policy principals.


<br><br>

### :file_folder: Setting the kms_owner_principal_list module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket


    // Optional Variables with module defined default values assigned
    kms_owner_principal_list    = ['arn:aws:iam::123456789101::root', 'arn:aws:iam::109876543210::root']
}
```




<br><br><br>## :white_check_mark: kms_admin_principal_list


<br>

![Optional](images/neon_optional.png)

<br>

This variable is used to define a list of users/roles that will be added to the KMS Key Administrator policy statement block. If a list of roles/users (including a list of a single user or role) is provided, then a KMS key Administrator policy will be generated automatically and appended to the key policy that will be applied to the provisioned CMK. If this variable is left empty or not included in the module call, then the KMS key administrator policy statement **will not be included** in the KMS key policy. The account root owner will still have kms:* permissions, but no additional administrators will be added. IAM policies can be constructed post key creation in order to grant permissions, including administration permissions to users/roles later by the key owner. Image:


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> The key administrator policy statement determines what users/roles have administrative rights on the provisioned KMS key. Key administrators can modify the key and the key policy, but they are not granted usage of the key, or the ability to manage grants for the key. If a key administrator requires usage permissions, then they would also need to be added to the key usage policy statement.


<br><br>

### :file_folder: Declaration of kms_admin_principal_list within the modules variables.tf file

```terraform
variable "kms_admin_principal_list" {
    type        = list
    description = "List of users/roles that will be key administrators of the provisioned KMS CMK"
    default     = []
}


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> You can not assign an IAM group as a policy principal, only IAM users/roles are allowed as policy principals.


<br><br>

### :file_folder: Setting the kms_admin_principal_list module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket


    // Optional Variables with module defined default values assigned
    kms_admin_principal_list    = ['arn:aws:iam::123456789101:role/AWS-KMS-Admin-Role']
}
```




<br><br><br>## :white_check_mark: kms_user_principal_list


<br>

![Optional](images/neon_optional.png)

<br>

This variable is used to define a list of users/roles that will be added to the KMS Key usage policy statement block. If a list of roles/users (including a list of a single user or role) is provided, then a KMS key usage policy will be generated automatically and appended to the key policy that will be applied to the provisioned CMK. If this variable is left empty or not included in the module call, then the KMS key usage policy statement **will not be included** in the KMS key policy. The account root owner will still have kms:* permissions, but no additional key users will be added. IAM policies can be constructed post key creation in order to grant permissions, including key usage permissions to users/roles later by the key owner or a key administrator. Image:


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> The key usage policy statement determines what users/roles have rights to encrypt, decrypt, re-encrypt, and generate data key operations with the provisioned CMK. Any users/roles that are included in this policy statement have no other rights on the key unless they are also added to one of the other key policy statement blocks also.


<br><br>

### :file_folder: Declaration of kms_user_principal_list within the modules variables.tf file

```terraform
variable "kms_user_principal_list" {
    type        = list
    description = "List of users/roles that will be granted usage of the provisioned KMS CMK."
    default     = []
}


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> You can not assign an IAM group as a policy principal, only IAM users/roles are allowed as policy principals.


<br><br>

### :file_folder: Setting the kms_user_principal_list module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket


    // Optional Variables with module defined default values assigned
    kms_user_principal_list     = ['arn:aws:iam::123456789101:role/AWS-RDS-Service-Role', 'arn:aws:iam::123456789101:user/rnason']
}
```




<br><br><br>## :white_check_mark: kms_resource_principal_list


<br>

![Optional](images/neon_optional.png)

<br>

This variable is used to define a list of users/roles that will be added to the KMS Key resource grant policy statement block. If a list of roles/users (including a list of a single user or role) is provided, then a KMS key resource grant policy will be generated automatically and appended to the key policy that will be applied to the provisioned CMK. If this variable is left empty or not included in the module call, then the KMS key resource grant policy statement **will not be included** in the KMS key policy. The account root owner will still have kms:* permissions, but no additional key resource grant permissions will be added. IAM policies can be constructed post key creation in order to grant permissions, including key grantee permissions to users/roles later by the key owner or a key administrator. Image:


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> The key resource grant policy statement determines what users/roles have rights to list, create, and revoke grants on the provisioned CMK. Key grants are a way of providing usage of the CMK temporarily. A user/role that has key grant or resource rights is allowed to grant applications, services, or resources a limited time pass to use the CMK and then revoke that pass when the application, service, or resource has completed the operation that required access to the key. No other rights on the key are given unless the user/role is also added to one of the other key policy statement blocks also.


<br><br>

### :file_folder: Declaration of kms_resource_principal_list within the modules variables.tf file

```terraform
variable "kms_resource_principal_list" {
    type        = list
    description = "List of users/roles that will be granted permissions to create/list/delete temporary grants to the provisioned KMS CMK."
    default     = []
}


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> You can not assign an IAM group as a policy principal, only IAM users/roles are allowed as policy principals.


<br><br>

### :file_folder: Setting the kms_resource_principal_list module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket


    // Optional Variables with module defined default values assigned
    kms_resource_principal_list = ['arn:aws:iam::123456789101:role/AWS-RDS-Service-Role', 'arn:aws:iam::123456789101:user/rnason']
}
```




<br><br><br>## :white_check_mark: kms_tags


<br>

![Optional](images/neon_optional.png)

<br>

This variable should contain a map of tags that will be assigned to the KMS CMK upon creation. Any tags contained within the `kms_tags` map variable will be passed to the module and automatically merged with a few tags that are also automatically created when the module is executed. The automatically generated tags are as follows:
* __Name__ - This tag is assigned the value from the `kms_key_alias_name` required variable that is passed during module execution * __Created_By__ - This tag is assigned the value of the aws user that was used to execute the Terraform module to create the KMS CMK. It uses the Terraform `aws_caller_identity {}` data source provider to obtain the User_Id value. This tag will be ignored for any future executions of the module, ensuring that its value will not be changed after it's initial creation. * __Creator_ARN__ - This tag is assigned the ARN value of the aws user that was used to execute the Terraform module to create the KMS CMK. It uses the Terraform `aws_caller_identity {}` data source provider to obtain the User_ARN value. This tag will be ignored for any future executions of the module, ensuring that its value will not be changed after it's initial creation. * __Creation_Date__ - This tag is assigned a value that is obtained by the Terraform `timestamp()` function. This tag will be ignored for any future executions of the module, ensuring that its value will not be changed after it's initial creation. * __Updated_On__ - This tag is assigned a value that is obtained by the Terraform `timestamp()` function. This tag will be updated on each future execution of the module to ensure that it's value displays the last `terraform apply` date.


<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> The key administrator policy statement determines what users/roles have administrative rights on the provisioned KMS key. Key administrators can modify the key and the key policy, but they are not granted usage of the key, or the ability to manage grants for the key. If a key administrator requires usage permissions, then they would also need to be added to the key usage policy statement.


<br><br>

### :file_folder: Declaration of kms_tags within the modules variables.tf file

```terraform
variable "kms_tags" {
    type        = map
    description = "Specify any tags that should be added to the KMS CMK being provisioned."
    default     = {
        Provisioned_By = "Terraform"
        Module_GitHub_URL = "https://github.com/CloudMage-TF/AWS-KMS-Module.git"
    }
}




<br><br>

### :file_folder: Setting the kms_tags module variable within a projects root main.tf file

```terraform
module "kms" {
    source = "git@github.com:rnason/ActionsTest?ref=v1.1.0"

    // Required Variables
    kms_key_alias_name  = prod/s3
    kms_key_description = KMS key provisioned to encrypt prod s3 bucket


    // Optional Variables with module defined default values assigned
    kms_tags = {
        Provisioned_By = "Terraform"
        Module_GitHub_URL = "https://github.com/CloudMage-TF/AWS-KMS-Module.git"
        Environment = "Prod"
    }
}
```




<br><br><br>

# Module Example Usage

An example of how to use this module can be found within the `example` directory of this repository.

<br><br>

# Variables and TFVar Reference File Templates

The following code blocks can be used or appended to an existing `variables.tf` file or `terraform.tfvars` file respectively within the project root consuming this module. Optional Variables are commented out and have their values set to the default values defined in the module's variables.tf/terraform.tfvars respective file. If the values of any optional variables do not need to be changed, then they do not need to be redefined or included in the project root. If they do need to be changed, then add them to the root project and change the values according to the project requirements.

<br><br>

## :file_folder: Module variables.tf Reference File

```terraform
###########################################################################
# Required rnason/ActionsTest Module Vars:                             #
#-------------------------------------------------------------------------#
# The following variables require consumer defined values to be provided. #
###########################################################################
variable "kms_key_alias_name" {
    type        = string
    description = "The alias that will be assigned to the provisioned KMS CMK. This value will be appended to alias/ within the module automatically."
}

variable "kms_key_description" {
    type        = string
    description = "The description that will be applied to the provisioned KMS Key."
}


###########################################################################
# Optional rnason/ActionsTest Module Vars:                             #
#-------------------------------------------------------------------------#
# The following variables have default values already set by the module.  #
# They will not need to be included in a project root module variables.tf #
# file unless a non-default value needs be assigned to the variable.      #
###########################################################################
variable "kms_owner_principal_list" {
    type        = list
    description = "List of users/roles/accounts that will own and have kms:* on the provisioned CMK."
    default     = []
}
variable "kms_admin_principal_list" {
    type        = list
    description = "List of users/roles that will be key administrators of the provisioned KMS CMK"
    default     = []
}
variable "kms_user_principal_list" {
    type        = list
    description = "List of users/roles that will be granted usage of the provisioned KMS CMK."
    default     = []
}
variable "kms_resource_principal_list" {
    type        = list
    description = "List of users/roles that will be granted permissions to create/list/delete temporary grants to the provisioned KMS CMK."
    default     = []
}

variable "kms_tags" {
    type        = map
    description = "Specify any tags that should be added to the KMS CMK being provisioned."
    default     = {
        Provisioned_By = "Terraform"
        Module_GitHub_URL = "https://github.com/CloudMage-TF/AWS-KMS-Module.git"
    }
}
```

<br><br>

## :file_folder: Module TFVars Reference File

```terraform
###########################################################################
# Required rnason/ActionsTest Module Vars:                             #
#-------------------------------------------------------------------------#
# The following variables require consumer defined values to be provided. #
###########################################################################
kms_key_alias_name  = "Value Required"
kms_key_description = "Value Required"


###########################################################################
# Optional rnason/ActionsTest Module Vars:                             #
#-------------------------------------------------------------------------#
# The following variables have default values already set by the module.  #
# They will not need to be included in a project root module variables.tf #
# file unless a non-default value needs be assigned to the variable.      #
###########################################################################
# kms_owner_principal_list    = []
# kms_admin_principal_list    = []
# kms_user_principal_list     = []
# kms_resource_principal_list = []

# kms_tags = {
#   Provisioned_By = "Terraform"
#   Module_GitHub_URL = "https://github.com/CloudMage-TF/AWS-KMS-Module.git"
}
```

<br><br>

# Module Outputs Reference File Templates

The template will finally create the following outputs that can be pulled and used in subsequent terraform runs via data sources. The outputs will be written to the Terraform state file. When using and calling the module within a root project, the output values of the module are available to the project root by simply referencing the module outputs from the root project `outputs.tf` file.

<br><br>

## :file_folder: Module outputs.tf Reference File

```terraform
##############################################
# rnason/ActionsTest Outputs:             #
##############################################
output "kms_key_id" {
    aws_kms_key.this.id
}
output "kms_key_arn" {
    aws_kms_key.this.arn
}
output "kms_key_alias" {
    aws_kms_alias.this.arn
}
```

<br><br>

## :file_folder: Module Output Usage Reference File

```terraform
##############################################
# rnason/ActionsTest Outputs:             #
##############################################
output "kms_key_id" {
    value = module.kms.aws_kms_key.this.id
}
output "kms_key_arn" {
    value = module.kms.aws_kms_key.this.arn
}
output "kms_key_alias" {
    value = module.kms.aws_kms_alias.this.arn
}
```

<br>

> :spiral_notepad: &nbsp;[__Note:__](Note) <br> When referencing the module outputs be sure that the output value contains the identifier given to the module call. As an example, if the module was defined as `module "kms" {}` then the output reference would be constructed as `module.kms.kms_key_id`.

<br><br>

# Terraform Requirements

* [Terraform](https://www.terraform.io/)
* [GIT](https://git-scm.com/download/win)
* [AWS-Account](https://https://aws.amazon.com/)

<br><br>

# Recommended Terraform Utilities

* [Terraform for VSCode](https://github.com/mauve/vscode-terraform)
* [Terraform Config Inspect](https://github.com/hashicorp/terraform-config-inspect)

<br><br>

# Contacts and Contributions

This project is owned by [CloudMage](rnason@cloudmage.io)

* [rnason](https://github.com/rnason)

<br>

To contribute, please:

* Fork the project
* Create a local branch
* Submit Changes
* Create A Pull Request