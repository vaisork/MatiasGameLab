# Colaborar en Vintage Telnet

Leer primero `docs/CONTEXTO_CONTINUIDAD.md`, `CONTENT_CONTRACT.md` y `docs/ARCHITECTURE.md`. La profundización narrativa está en pausa hasta nueva autorización. El código narrativo guardado más reciente no ha sido desplegado en Raspberry.

El repositorio incluye servidor, cliente, contenido regional, ilustraciones WebP/PNG, modelos GLB y librerías visuales locales, tests, scripts y evidencia de revisión. `README.md` explica cómo instalar dependencias Python y generar credenciales privadas propias para una instalación de desarrollo. No copiar la DB de desarrollo sobre producción ni usar jugadores reales para pruebas. Cada colaborador debe crear su instancia aislada.

Para obtener una copia completa sin GitHub se entrega `vintage-telnet-git.bundle`: `git clone vintage-telnet-git.bundle vintage-telnet`. Conservar el historial y crear una rama para cada cambio. El tar.gz es una instantánea sin historial. El proyecto está en MatiasGameLab, carpeta vintage-telnet-2; trabajar desde main actualizado y abrir ramas/PR contra ese repositorio.

`runtime/`, bases de datos, respaldos, archivos env y fotos familiares originales no se distribuyen. Sus equivalentes artísticos integrados al juego están en `client/art/players`. No hace falta conocer secretos de Javier para programar o ejecutar una nueva instancia.

Antes de integrar: pruebas pertinentes, revisión real del recorrido o interfaz afectada, indicar si se utilizó DB temporal o estado interceptado, y describir límites. Mantener respuestas/diálogos claros para niños, acciones coherentes con estado real y canon. No añadir arquitecturas paralelas, habitaciones innecesarias ni dependencias externas de assets privados.
