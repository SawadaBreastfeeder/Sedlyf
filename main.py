import os

import time

from telegram.ext import Updater, CommandHandler

from telegram import InputFile

# Telegram bot token

TOKEN = '6174260573:AAHPQe3TgWw8CmAjFXdKtM7rGl6oxmv_Tj4'

# Create an instance of the Updater class

updater = Updater(token=TOKEN, use_context=True)

# Define the handler function for the '/start' command

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the File Renamer Bot!")

# Define the handler function for the '/rename' command

def rename_file(update, context):

    # Check if a filename is provided

    if len(context.args) == 0:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a filename to rename.")

        return

    

    file_name = " ".join(context.args)

    file_id = update.message.document.file_id

    

    # Download the file

    context.bot.send_message(chat_id=update.effective_chat.id, text="Downloading file...")

    start_time = time.time()

    file_path = context.bot.get_file(file_id).download()

    end_time = time.time()

    download_time = end_time - start_time

    download_speed = os.path.getsize(file_path) / download_time / 1024  # in KB/s

    

    # Rename the file

    renamed_file_path = "renamed_" + file_name

    context.bot.send_message(chat_id=update.effective_chat.id, text="Renaming file...")

    os.rename(file_path, renamed_file_path)

    

    # Upload the renamed file

    context.bot.send_message(chat_id=update.effective_chat.id, text="Uploading renamed file...")

    start_time = time.time()

    context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(renamed_file_path))

    end_time = time.time()

    upload_time = end_time - start_time

    upload_speed = os.path.getsize(renamed_file_path) / upload_time / 1024  # in KB/s

    

    # Send the summary

    summary = f"File renamed and uploaded successfully!\n\nDownload Speed: {download_speed:.2f} KB/s\nUpload Speed: {upload_speed:.2f} KB/s"

    context.bot.send_message(chat_id=update.effective_chat.id, text=summary)

    

    # Remove the files

    os.remove(renamed_file_path)

# Add handlers to the updater

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('rename', rename_file))

# Start the bot

updater.start_polling()

