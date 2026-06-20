import yaml
import sys

def load_locale(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_all_key_values(data, prefix=''):
    """Returns a dict of key->value for all string leaf nodes."""
    kv = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                kv.update(get_all_key_values(v, new_prefix))
            elif isinstance(v, str):
                kv[new_prefix] = v
            # ignore non-string values like numbers
    return kv

def main():
    en_data = load_locale('./locales/en.yaml')
    zh_data = load_locale('./locales/zh-TW.yaml')
    
    en_kv = get_all_key_values(en_data)
    zh_kv = get_all_key_values(zh_data)
    
    # Keys we need from screener explanation
    needed_keys = {
        # from provider direct t() calls
        'screener.explanation.fallback',
        'screener.explanation.implication.dividend',
        'screener.explanation.implication.growth',
        'screener.explanation.implication.value',
        'screener.explanation.filter.revenue_positive',
        'screener.explanation.filter.industry_match',
        'screener.explanation.filter.per_range',
        'screener.explanation.filter.div_range',
        'screener.explanation.implication.custom_many',
        'screener.explanation.implication.custom_fallback',
        'screener.explanation.implication.default',
        'screener.explanation.filter.all_industries',
        # from screener_templates.yaml (template keys)
        'screener.explanation.preset.dividend.high_yield',
        'screener.explanation.preset.dividend.stable',
        'screener.explanation.preset.dividend.fallback',
        'screener.explanation.preset.dividend.implication',
        'screener.explanation.preset.growth.strong',
        'screener.explanation.preset.growth.moderate',
        'screener.explanation.preset.growth.fallback',
        'screener.explanation.preset.growth.implication',
        'screener.explanation.preset.value.deep_value',
        'screener.explanation.preset.value.moderate_value',
        'screener.explanation.preset.value.fallback',
        'screener.explanation.preset.value.implication',
        'screener.explanation.custom_filter.revenue_positive',
        'screener.explanation.custom_filter.industry_match',
        'screener.explanation.custom_filter.per_range',
        'screener.explanation.custom_filter.div_range',
        'screener.explanation.custom_filter.fallback',
        'screener.explanation.custom_filter.implication',
        'screener.explanation.disclaimer',
    }
    
    missing_in_en = []
    empty_in_en = []
    for k in needed_keys:
        if k not in en_kv:
            missing_in_en.append(k)
        elif not en_kv[k].strip():
            empty_in_en.append(k)
            
    missing_in_zh = []
    empty_in_zh = []
    for k in needed_keys:
        if k not in zh_kv:
            missing_in_zh.append(k)
        elif not zh_kv[k].strip():
            empty_in_zh.append(k)
    
    if missing_in_en:
        print("Missing keys in en.yaml:")
        for k in sorted(missing_in_en):
            print(f"  {k}")
    else:
        print("No missing keys in en.yaml")
        
    if empty_in_en:
        print("Empty keys in en.yaml:")
        for k in sorted(empty_in_en):
            print(f"  {k}: '{en_kv[k]}'")
    else:
        print("No empty keys in en.yaml")
        
    if missing_in_zh:
        print("Missing keys in zh-TW.yaml:")
        for k in sorted(missing_in_zh):
            print(f"  {k}")
    else:
        print("No missing keys in zh-TW.yaml")
        
    if empty_in_zh:
        print("Empty keys in zh-TW.yaml:")
        for k in sorted(empty_in_zh):
            print(f"  {k}: '{zh_kv[k]}'")
    else:
        print("No empty keys in zh-TW.yaml")
        
    if not missing_in_en and not empty_in_en and not missing_in_zh and not empty_in_zh:
        print("\nAll locale keys are present and non-empty.")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())