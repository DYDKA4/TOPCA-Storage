## Dependencies

Apt packages:
- curl
- python, python-pip
- ansible

Python packages:
- PyYAML==6.0
- Flask==2.1.2
- Werkzeug==2.1.2
- redis==4.3.4
- nebula3-python==3.1.0


## Configuration

Configuration of the project is stored in the **./config.py** file. Example:

```python
## Vault
IP_address = '10.100.149.228'  # IP address where Nebula Graph is deployed
DataBasePort = 9669  # Port to connect to Nebula Graph. Default is 9669
UserName = 'root'  # UserName in Nebula Graph. Default is "root"
UserPassword = 'password'  # Password in Nebula Graph. Default is "password"
WorkSpace = 'Tosca_Templates'  # Work Space in Nebula Graph
RedisPort = 6380  # Port to connect to Nebula Graph. Default is 6379
```
Configuration of the virtual machine is stored in the **.deployment/inventory.yaml** file. Example:
```yaml
## Vault
virtual_machines:
  hosts:
    vm01:
      ansible_host: 10.100.148.224
  vars:
    ansible_user: ubuntu
```

# Getting started

### Configure Virtual Machine with Nebula
Before start check which ip is specified for the virtual machine in the **.deployment/inventory.yaml**
After this open in cmd directory of this project.
```bash
cd ./deplyment/
ansible-playbook -i inventory.yaml playbook.yaml
```

### Configure venv
Install all package from dependencies. You should be careful with version of python package. 

### Start flask API
After this preparation run this bash script
```bash
nohup python run.py &
```
You successfully launch flask API.

