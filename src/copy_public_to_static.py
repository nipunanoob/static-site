import os 
import shutil

def copy_content_src_to_dst(src, dst, clear_flag):
    if os.path.exists(dst):
        if clear_flag: #runs only at first function call to prevent clearing multiple times
            shutil.rmtree(dst)
            print(f"Cleared {dst}")
            os.mkdir(dst)
        if os.path.exists(src):
            content_list = os.listdir(src)
            for content in content_list:
                content_path = os.path.join(src, content)
                if not os.path.isfile(content_path): # if content is directory
                    subdir_path = os.path.join(dst, content)
                    print(f"Making directory {subdir_path}")
                    os.mkdir(subdir_path)
                    copy_content_src_to_dst(content_path, subdir_path, False)
                else: #if content is file
                    print(f"Moving file {content} from {src} to {dst}")
                    shutil.copy(content_path, dst)
        else:
            raise FileNotFoundError(f"Source directory {src} does not exist")
    else:
        raise FileNotFoundError(f"Destination directory {dst} does not exist")
                    
