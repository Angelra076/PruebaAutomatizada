import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Crear carpeta para capturas si no existe
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Configuración del WebDriver
driver_path = "docs/chromedriver-win64/chromedriver.exe"  # Cambia la ruta si es necesario
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Variables para el reporte HTML
report_content = """
<html>
<head><title>Reporte de Prueba Automatizada</title></head>
<body>
    <h1>Reporte de Prueba Automatizada</h1>
    <p><strong>Fecha y hora de la prueba:</strong> {}</p>
    <h2>Pasos de la prueba:</h2>
    <ul>
        <li><strong>Acción 1:</strong> Abrir la página https://demoqa.com/text-box</li>
        <li><strong>Acción 2:</strong> Ingresar datos en el formulario.</li>
        <li><strong>Acción 3:</strong> Enviar el formulario.</li>
        <li><strong>Acción 4:</strong> Validar los resultados.</li>
    </ul>
    <h2>Capturas de Pantalla:</h2>
"""

try:
    # Iniciar prueba
    print("Iniciando prueba en https://demoqa.com/text-box")
    driver.get("https://demoqa.com/text-box")
    driver.maximize_window()

    # Esperar un momento para asegurar que todo cargue correctamente
    time.sleep(2)

    # Captura inicial de la página
    screenshot_path = "screenshots/01_pagina_inicial.png"
    driver.save_screenshot(screenshot_path)
    report_content += f'<p><img src="{screenshot_path}" alt="Página inicial"></p>'

    # Llenar el formulario
    driver.find_element(By.ID, "userName").send_keys("John Doe")
    driver.find_element(By.ID, "userEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "currentAddress").send_keys("123 Main St, Springfield")
    driver.find_element(By.ID, "permanentAddress").send_keys("456 Elm St, Shelbyville")
    screenshot_path = "screenshots/02_formulario_llenado.png"
    driver.save_screenshot(screenshot_path)
    report_content += f'<p><img src="{screenshot_path}" alt="Formulario lleno"></p>'

    # Eliminar anuncios si existen
    ads_iframe = driver.find_elements(By.ID, "google_ads_iframe_/21849154601,22343295815/Ad.Plus-Anchor_0__container__")
    for ad in ads_iframe:
        driver.execute_script("arguments[0].remove();", ad)

    # Hacer clic en el botón de submit
    wait = WebDriverWait(driver, 10)
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    submit_button.click()
    time.sleep(2)

    # Captura después de enviar el formulario
    screenshot_path = "screenshots/03_formulario_enviado.png"
    driver.save_screenshot(screenshot_path)
    report_content += f'<p><img src="{screenshot_path}" alt="Formulario enviado"></p>'

    # Validar resultados
    output_name = driver.find_element(By.ID, "name").text
    output_email = driver.find_element(By.ID, "email").text
    output_current_address = driver.find_element(By.XPATH, "//p[@id='currentAddress']").text
    output_permanent_address = driver.find_element(By.XPATH, "//p[@id='permanentAddress']").text

    assert "John Doe" in output_name
    assert "johndoe@example.com" in output_email
    assert "123 Main St, Springfield" in output_current_address
    assert "456 Elm St, Shelbyville" in output_permanent_address

    report_content += """
    <h2>Resultados de la prueba:</h2>
    <p><strong>Nombre:</strong> {} </p>
    <p><strong>Email:</strong> {} </p>
    <p><strong>Dirección actual:</strong> {} </p>
    <p><strong>Dirección permanente:</strong> {} </p>
    <p>La prueba se completó exitosamente.</p>
    """.format(output_name, output_email, output_current_address, output_permanent_address)

except Exception as e:
    screenshot_path = "screenshots/error.png"
    driver.save_screenshot(screenshot_path)
    report_content += f'<p><img src="{screenshot_path}" alt="Error en la prueba"></p>'
    report_content += f"<p>Se produjo un error: {e}</p>"

finally:
    driver.quit()

# Finalizar el reporte HTML
report_content += "</body></html>"

# Guardar el reporte en un archivo HTML
with open("reporte_prueba.html", "w") as file:
    file.write(report_content)

print("Reporte HTML generado exitosamente.")
