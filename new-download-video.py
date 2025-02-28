#!/usr/bin/env python3
# coding: utf-8
#
# Copyright (C) 2023, Diego Cambiaso
# Modified 2025
# GNU General Public License v3.0

"""
Script para descargar videos de YouTube con opciones ampliadas.
Este script es para propósitos educativos.
"""

__version__ = "1.6.0"

import os
import sys
import argparse
from typing import Optional, Union
from pytube import YouTube

def download_video(url: str, output_path: Optional[str] = None, 
                  resolution: Optional[str] = None, 
                  filename: Optional[str] = None) -> Union[str, None]:
    """
    Descarga un video de YouTube desde la URL proporcionada.
    
    Args:
        url: URL del video de YouTube.
        output_path: Ruta donde se guardará el video. Si es None, usa el directorio actual.
        resolution: Resolución del video ("highest", "lowest", "720p", "480p", etc).
        filename: Nombre personalizado del archivo descargado.
        
    Returns:
        Ruta del archivo descargado o None si hubo un error.
    """
    try:
        # Validar la URL
        if not url or "youtube.com" not in url and "youtu.be" not in url:
            raise ValueError("La URL proporcionada no parece ser de YouTube")
            
        print(f"Obteniendo información del video: {url}")
        yt = YouTube(url)
        
        # Mostrar información del video
        print(f"Título: {yt.title}")
        print(f"Autor: {yt.author}")
        print(f"Duración: {yt.length} segundos")
        
        # Seleccionar stream según la resolución solicitada
        if resolution == "highest" or resolution is None:
            stream = yt.streams.get_highest_resolution()
        elif resolution == "lowest":
            stream = yt.streams.get_lowest_resolution()
        else:
            # Intenta obtener la resolución específica
            stream = yt.streams.filter(res=resolution, progressive=True).first()
            if not stream:
                print(f"Resolución {resolution} no disponible. Usando la más alta disponible.")
                stream = yt.streams.get_highest_resolution()
        
        # Preparar la ruta de salida
        if not output_path:
            output_path = os.getcwd()
        elif not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
            
        # Preparar el nombre del archivo
        if filename:
            # Aseguramos que tenga la extensión correcta
            if not filename.endswith(f".{stream.subtype}"):
                filename = f"{filename}.{stream.subtype}"
        else:
            filename = None  # pytube generará un nombre basado en el título
            
        print(f"Descargando video ({stream.resolution})...")
        output_file = stream.download(output_path=output_path, filename=filename)
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Tamaño en MB
        
        print(f"Descarga completada exitosamente:")
        print(f"- Archivo: {os.path.basename(output_file)}")
        print(f"- Tamaño: {file_size:.2f} MB")
        print(f"- Ubicación: {os.path.abspath(output_file)}")
        
        return output_file
        
    except (OSError, RuntimeError, ValueError) as e:
        print(f"Error: {str(e)}")
    except KeyboardInterrupt:
        print("\nDescarga interrumpida por el usuario")
    except Exception as e:
        print(f"Error inesperado durante la descarga: {str(e)}")
    
    return None

def main():
    """Función principal que maneja la línea de comandos."""
    parser = argparse.ArgumentParser(description="Descargador de videos de YouTube")
    parser.add_argument("url", nargs="?", help="URL del video de YouTube")
    parser.add_argument("-o", "--output", help="Carpeta donde guardar el video")
    parser.add_argument("-r", "--resolution", 
                        choices=["highest", "lowest", "1080p", "720p", "480p", "360p"], 
                        default="highest",
                        help="Resolución del video")
    parser.add_argument("-f", "--filename", help="Nombre personalizado del archivo")
    parser.add_argument("-v", "--version", action="version", 
                       version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    # Si no se proporciona URL por línea de comandos, pedirla
    url = args.url
    if not url:
        url = input("Ingrese la URL del video de YouTube: ")
    
    download_video(url, args.output, args.resolution, args.filename)
    
    print("Programa finalizado")

if __name__ == "__main__":
    main()
