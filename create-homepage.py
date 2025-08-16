import os

template = """
<uhml> <!-- 根 -->
  <loader> <!-- 定义加载器 -->
    %(define)s
    <meta> <!-- 元数据 -->
      <filesource alias="metadata">%(meta_url)</filesource> <!-- 元数据文件源 -->
    </meta>
  </loader>
  <card id="0"> <!-- 卡片，文件的基本单元 -->
    <filesource alias="card">0.card</filesource> <!-- 卡片实现源 -->
    <filesource alias="cass">0.CaSS</filesource> <!-- 卡片样式源 -->
  </card>
  <card id="1">
    <filesource alias="card">1.card</filesource> <!-- 卡片内容简单时，可以不使用 CaSS -->
  </card>
</uhml>
"""

meta_template = """
<uhmeta>
  <name>%(name)s</name>
  <license>%(lic)s</license>
  <author>%(author)s</author>
  <email>%(email)s</email>
  <version>%(version)s</version>
  %(custom)s
</uhmeta>
"""


def _safe_input(prompt: str, default="") -> str:
    """
    安全输入
    Args:
        prompt (str): 提示
    Returns:
        str: 输入内容
    """
    if input(f"{prompt}（留空以使用默认值 {default}）：\n>") == "":
        return default
    return input(prompt)


def get_defines() -> str:
    """
    获取加载器定义
    Returns:
        str: 加载器定义值
    """
    _define: dict = eval(_safe_input("请输入加载器定义（键值对）"))
    if _define:
        defines: list[str] = []
        for key, value in _define.items():
            defines.append(f"<define {key}=\"{value}\"/>")
    elif not _define:
        defines = ["<define continuous=\"true\"/>", "<define order=\"increase\"/>"]
    else:
        defines = []

    del _define
    define = "\n".join(defines)

    return define


def get_metadata() -> str:
    """
    获取元数据文件源
    Returns:
        str: 元数据文件源（确定存在的路径）
    """
    meta: str = _safe_input("请输入元数据文件源")
    if not os.path.exists(meta):
        print("元数据文件不存在，正在创建")
        create_metadata()
        get_metadata()

    if not meta.endswith(".uhmeta"):
        return ""

    return meta


def create_metadata() -> bool:
    """
    创建元数据文件
    Returns:
        bool: 是否成功创建
    """
    meta: str = _safe_input("请输入新元数据文件源")
    if not meta or not meta.endswith(".uhmeta") or os.path.exists(meta):
        return False

    name = _safe_input("输入主页名称", default="MyHomepage")
    lic = _safe_input("输入主页所使用的授权协议", default="MIT")
    author = _safe_input("输入主页作者名称", default="Unknown")
    email = _safe_input("输入主页作者的电子邮箱", default="Unknown")
    version = _safe_input("输入主页版本", default="v1.0.0")
    _custom = _safe_input("输入自定义字段（键值对）")

    if _custom:
        customs = []
        for key, value in eval(_custom).items():
            customs.append(f"<custom alias=\"{key}\">{value}</custom>")

        custom = "\n".join(customs)
        del _custom, customs

    else:
        custom = ""

    metadata = meta_template.format(name=name, lic=lic, author=author, email=email, version=version, custom=custom)

    with open(meta, "w", encoding="utf-8") as f:
        f.write(metadata)

    return True


if __name__ == "__main__":
    print("写入加载器...")
    uhml = template.format(define=get_defines(), meta_url=get_metadata())
