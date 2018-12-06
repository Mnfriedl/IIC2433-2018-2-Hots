# IIC2433-2018-2-Hots

###### Authors: 

- Maximiliano Friedl ([Mnfriedl](https://github.com/Mnfriedl))
- Felipe Gomez ([Fagomez2](https://github.com/fagomez2))



## Needed dependencies

### Git submodules

We are using Blizzard's [heroprotocol](https://github.com/Blizzard/heroprotocol) to parse the `.StormReplay` files, so if you intend to parse *replays* with our script inside the `/Preprocessing` folder, you must clone the repo including submodules. For this, use:

`git clone https://github.com/Mnfriedl/IIC2433-2018-2-Hots --recursive`

### Python libraries

#### Preprocessing:

- `boto3`
- `psycopg2`
- `pandas`
- `sqlalchemy` (used to export the database into a `.csv` file)
- `requests`
- `awscli`: for this, you need to run `pip install awscli` and then `aws configure`, or you won't be able to download files from the Amazon AWS S3 bucket. For more information, read [this](https://aws.amazon.com/es/cli/) and [this](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

#### Models:

- `pandas`
- `numpy`
- `sklearn`

