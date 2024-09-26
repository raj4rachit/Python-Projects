import os

import openai

openai.organization = "org-328e8dyLYeiOCMSqJ2dmM8Dw"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
