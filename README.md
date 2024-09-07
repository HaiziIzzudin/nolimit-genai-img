### What if you can generate AI images, no payment required, no sign-in required* and _unlimited_**?
That is what this repo/ script is aimed to do.

### How to run this script?
#### For first timer, starts from step 1
#### Otherwise for past users, start from step 6
1. Install [python version 3.11.9](https://www.python.org/downloads/release/python-3119/) and latest [git](https://git-scm.com/downloads) in your computer.<br>
***Also has been tested on Python 3.11.7 and 3.9.2***
2. Launch terminal and test your installed python and git version.
```bash
python -V
```
```bash
# the output should be
# Python 3.11.9
```
```bash
git -v
```
```bash
# the output should be
# git version <version_number>.<platform>
```
3. Git clone this repository
```bash
git clone https://github.com/HaiziIzzudin/nolimit-genai-img.git
```
4. Change your working directory to cloned repository
```bash
cd nolimit-genai-img
```
5. Create python virtual environment
```bash
python -m venv venv
```
6. Launch python virtual environment
```bash
./venv/Scripts/activate
```
```bash
# There should be an indication that you are currently in a venv. Example:
# (venv) $
```
7. Install all required module for this script
```bash
pip install -r requirements.txt
```
```bash
# some fastapi components may failed to install. PLease install it manually:
pip install fastapi "fastapi[all]" fastapi-cli
```
8. Edit config.toml file included in the repository. **Please follow the instructions written in config.toml or script will fail!**.
9. Run inference. There are two modes that you can run, (a) _API Mode_, and (b) _WebDriver Mode_:

   a. API Mode (faster, but inference may fail and prone to API blocking)<br>
   [Please Read This before begin API Mode](docs/api_setup.md)
   ```bash
   python ./hf_api.py
   ```
      
   b. WebDriver Mode (slower, but more reliable and can interact even if script is quit unexpectedly)<br>
   [Please Read This before begin WebDriver Mode](docs/selenium_setup.md)
    
   ```bash
   python ./hf_selenium.py
   ```

11. Now we wait.
12. If image has successfully generated, script wil quit with no error, or if your config.toml configuration is to come by, should also launch your file explorer to the output folder.

.

.
### Method that makes this work
We uses the HuggingFace (HF) inference API, which is publicly available and accessible through Gradio, Warm Inference API or Selenium. The catch is that it's a free service, which means there are limits to how much you can use it. To get around these limits, we use a proxy. This method works pretty well, but it's not perfect. Sometimes it can take a while to get results, especially if a lot of people are using it at the same time and HF starts rate-limiting the proxies. And if HF goes down or decides to shut off their API, our script will stop working. We'll keep an eye on things and update our method if we need to.<br>
***It is recommended to provide your own HF token, since that is also has free generation.***<br>
Sometimes, it's just easier to pay for a service, and we're actually working on a paid image generation method that we think will be a good value. We'll let you know when it's ready.

One important thing to keep in mind, **don't even think about using this method to offer paid services**. That's **NOT ALLOWED** and is basically reselling something that's supposed to be free.

.

.

# Support my software development on [Ko-Fi](https://ko-fi.com/haiziizzudin)
#### *Thank you from the bottom of my heart ❤️*

.

.

### DISCLAIMER
###### By using this program, you acknowledge that it relies on the publicly available HuggingFace (HF) inference API and is subject to its limitations and terms of use. You agree not to use our method to offer paid services or resell the generated images in any way. You understand that this is strictly prohibited and may result in federal legal action. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. By using our method, you release us from any liability for any damages or losses resulting from its use, including but not limited to delays, errors, or discontinuation of the service. **ALL RIGHTS RESERVED**. All content, including but not limited to the image generation method, is protected by applicable copyright and intellectual property laws. No part of the copyrighted content may be reproduced, distributed, or transmitted in any form or by any means, electronic or mechanical, without the prior written permission of the copyright holder.
