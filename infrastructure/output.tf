output "public_ip_address" {
  value = azurerm_public_ip.load_ip.ip_address
}
