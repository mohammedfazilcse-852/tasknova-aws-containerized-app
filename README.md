
# TaskNova – AWS Containerized To-Do Application

A containerized Flask-based productivity application deployed on **AWS ECS Fargate** with Amazon RDS MySQL, Amazon ECR, Application Load Balancer, CloudWatch monitoring, and SNS alerts.

## Project Overview

TaskNova is a personal productivity application that allows users to create, view, complete, and delete tasks. The application is containerized using Docker and deployed on AWS using a highly available architecture across two Availability Zones.

## Key Features

- Add, view, complete, and delete tasks.
- Persistent task storage using Amazon RDS MySQL.
- Flask application with Gunicorn.
- Docker containerization.
- Private container image storage using Amazon ECR.
- ECS Fargate deployment with two tasks.
- Application Load Balancer for incoming HTTP traffic.
- AWS Secrets Manager for database credentials.
- CloudWatch logs and CPU monitoring.
- SNS email notifications.
- Version 2 deployment using ECS rolling updates.

## AWS Architecture

```text
                         Internet
                            |
                            v
                 Application Load Balancer
                            |
                 -----------------------
                 |                     |
                 v                     v
          ECS Fargate Task 1     ECS Fargate Task 2
             (AZ 1)                 (AZ 2)
                 |                     |
                 -----------------------
                            |
                            v
                    Amazon RDS MySQL
                      (Private DB)
                            
Additional AWS Services:
- Amazon ECR: Docker image storage
- AWS Secrets Manager: Database credentials
- Amazon CloudWatch: Logs and alarms
- Amazon SNS: Email notifications
- NAT Gateway: Outbound internet access
```

## AWS Infrastructure

**Region:** Asia Pacific (Mumbai) – `ap-south-1`

**VPC Configuration**

| Component | CIDR |
|---|---|
| VPC | 10.0.0.0/16 |
| Public Subnet 1 | 10.0.1.0/24 |
| Public Subnet 2 | 10.0.2.0/24 |
| Private App Subnet 1 | 10.0.11.0/24 |
| Private App Subnet 2 | 10.0.12.0/24 |
| Private DB Subnet 1 | 10.0.21.0/24 |
| Private DB Subnet 2 | 10.0.22.0/24 |

**Networking Components**
- VPC with six subnets across two Availability Zones.
- Internet Gateway for public internet access.
- NAT Gateway for outbound internet access from private application subnets.
- Separate route tables for public, application, and database subnets.
- Security groups controlling communication between the ALB, ECS tasks, RDS, and Bastion host.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python / Flask | Backend application |
| HTML / CSS | Frontend |
| MySQL | Database |
| Docker | Containerization |
| Amazon ECR | Container image registry |
| Amazon ECS Fargate | Container deployment |
| Application Load Balancer | Traffic distribution |
| Amazon RDS | Managed database |
| AWS Secrets Manager | Credential management |
| CloudWatch | Logs and monitoring |
| SNS | Email notifications |

## Deployment Process

1. Created a custom VPC and six subnets across two Availability Zones.
2. Configured Internet Gateway, NAT Gateway, route tables, and security groups.
3. Created an Amazon RDS MySQL database in private subnets.
4. Stored database credentials in AWS Secrets Manager.
5. Developed the Flask application and tested it locally.
6. Created a Docker image and pushed it to Amazon ECR.
7. Created an ECS Fargate cluster and task definition.
8. Deployed two ECS tasks in private application subnets.
9. Configured an Application Load Balancer and health checks.
10. Configured CloudWatch logging and CPU alarms.
11. Created an SNS email subscription for alarm notifications.
12. Built and deployed V2 using an ECS rolling deployment.

## Docker Commands

Build the Docker image:

```bash
docker build -t tasknova:1.0 .
```

Run locally:

```bash
docker run -p 5000:5000 tasknova:1.0
```

Build V2:

```bash
docker build -t tasknova:2.0 .
```

## Monitoring and Alerts

- CloudWatch log group: `/ecs/tasknova`
- ECS CPU utilization alarm configured with a 70% threshold.
- SNS topic: `tasknova-alerts`
- Email notifications tested successfully.

## Zero-Downtime Deployment

Implemented a V2 release using Amazon ECR and ECS rolling deployment.

- Built and pushed the V2 Docker image.
- Registered a new ECS task definition revision.
- Updated the ECS service to use V2.
- Monitored the deployment and target health.
- Verified that two tasks were running after deployment.
- Confirmed the updated application through the ALB.

## Security

- ECS tasks deployed in private application subnets.
- RDS deployed without public access.
- Database credentials injected through Secrets Manager.
- Security groups restrict traffic between application tiers.
- No database passwords are stored in the source code.

## Future Improvements

- Add HTTPS using AWS Certificate Manager.
- Configure a custom domain.
- Add CI/CD automation using GitHub Actions.
- Add automated database backups and recovery testing.

## Author

**Mohammed Fazil**

GitHub: [mohammedfazilcse-852](https://github.com/mohammedfazilcse-852)

LinkedIn: [Mohammed Fazil](https://www.linkedin.com/in/mohammed-fazil-95a5383a5/)
