terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}
 
provider "docker" {}
 
resource "docker_image" "nginx" {
  name = "nginx:latest"
}
 
resource "docker_container" "web" {
  name  = "web-terraform"
  image = docker_image.nginx.image_id
 
  ports {
    internal = 80
    external = 8081
  }
}