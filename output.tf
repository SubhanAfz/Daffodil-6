output "ubuntu_deployment_server_public_ip" {
    description = "Public IP of the Ubuntu Deployment Server"
    value = aws_instance.ubuntu_deployment_server.public_ip
}

output "ubuntu_deployment_server_id" {
    description = "ID of the Ubuntu Deployment Server"
    value = aws_instance.ubuntu_deployment_server.id
}