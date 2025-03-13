resource "aws_vpc" "test_vpc" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "test-vpc"
  }
}

# Public Subnet Definition
resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.test_vpc.id
  cidr_block = "10.0.1.0/24"

  availability_zone = "ap-south-1a"

  tags = {
    Name = "public-subnet"
  }
}

# Internet Gateway for Public Subnet
resource "aws_internet_gateway" "public_igw" {
  vpc_id = aws_vpc.test_vpc.id

  tags = {
    Name = "public-igw"
  }
}

# Public Route Table for the VPC
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block = "0.0.0.0/0"          # Default route for public access
    gateway_id = aws_internet_gateway.public_igw.id  # Routing through IGW
  }

  tags = {
    Name = "public-route-table"
  }
}

# Associate Public Subnet with Public Route Table
resource "aws_route_table_association" "public_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Private Subnet Definition
resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.test_vpc.id
  cidr_block = "10.0.2.0/24"

  availability_zone = "ap-south-1b"

  tags = {
    Name = "private-subnet"
  }
}

# Private Route Table for the VPC
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block = "10.0.0.0/16"
    gateway_id = "local"  # Default route within the VPC
  }

  tags = {
    Name = "private-route-table"
  }
}

# Associate Private Subnet with Private Route Table
resource "aws_route_table_association" "private_association" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_rt.id
}

# Security Group Definition
resource "aws_security_group" "test_sg" {
  name        = "test_sg"
  description = "Allow inbound SSH (port 22) and HTTP (port 80) traffic and all outbound traffic"
  vpc_id      = aws_vpc.test_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allows all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "test_sg"
  }
}

resource "aws_instance" "public_instance" {
  ami           = "ami-00bb6a80f01f03502"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_subnet.id
  associate_public_ip_address = "true"
  security_groups = [aws_security_group.test_sg.name]

  depends_on = [aws_security_group.test_sg]
}

resource "aws_instance" "private_instance" {
  ami           = "ami-00bb6a80f01f03502"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.private_subnet.id
  security_groups = [aws_security_group.test_sg.name]

  depends_on = [aws_security_group.test_sg]
}
