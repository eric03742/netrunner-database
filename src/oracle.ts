import fs from "fs/promises";
import path from "path";
import log from "loglevel";
import {
    SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
    SettypeEntity, CycleEntity, SetEntity,
    FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
    CardEntity, PrintingEntity, RulingEntity,
} from "netrunner-entities";


import { AppDataSource } from "./data-source";


/** 英文源数据通用字段 */
interface BaseSchema {
    /** 唯一标识符 */
    readonly id: string;
}

/** 英文源数据「阵营」 */
interface SideSchema extends BaseSchema {
    /** 阵营名称 */
    readonly name: string;
}

/** 英文源数据「派系」 */
interface FactionSchema extends BaseSchema {
    /** 派系名称 */
    readonly name: string;
    /** 派系描述 */
    readonly description: string;
    /** 派系颜色 */
    readonly color: string;
    /** 派系所属阵营ID */
    readonly side_id: string;
    /** 派系是否为迷你派系 */
    readonly is_mini: boolean;
}

/** 英文源数据「类型」 */
interface TypeSchema extends BaseSchema {
    /** 类型名称 */
    readonly name: string;
    /** 类型所属阵营ID */
    readonly side_id: string;
}

/** 英文源数据「子类型」 */
interface SubtypeSchema extends BaseSchema {
    /** 子类型名称 */
    readonly name: string;
}

/** 英文源数据「卡包类型」 */
interface SettypeSchema extends BaseSchema {
    /** 卡包类型名称 */
    readonly name: string;
    /** 卡包类型描述 */
    readonly description: string;
}

/** 英文源数据「循环」 */
interface CycleSchema extends BaseSchema {
    /** 循环名称 */
    readonly name: string;
    /** 循环旧版唯一标识符 */
    readonly legacy_code: string;
    /** 循环序号 */
    readonly position: number;
    /** 循环发行组 */
    readonly released_by: string;
}

/** 英文源数据「卡包」 */
interface SetSchema extends BaseSchema {
    /** 卡包名称 */
    readonly name: string;
    /** 卡包旧版唯一标识符 */
    readonly legacy_code: string;
    /** 卡包所属循环ID */
    readonly card_cycle_id: string;
    /** 卡包所属卡包类型ID */
    readonly card_set_type_id: string;
    /** 卡包发行日期 */
    readonly date_release: string;
    /** 卡包在循环中位置 */
    readonly position: number;
    /** 卡包卡牌数量 */
    readonly size: number;
    /** 卡包发行组 */
    readonly released_by: string;
}

/** 英文源数据「赛制」 */
interface FormatSchema extends BaseSchema {
    /** 赛制名称 */
    readonly name: string;
    /** 赛制历代环境 */
    readonly snapshots: SnapshotSchema[];
}

/** 英文源数据「环境」 */
interface SnapshotSchema extends BaseSchema {
    /** 环境开始时间 */
    readonly date_start: string;
    /** 环境使用卡池ID */
    readonly card_pool_id: string;
    /** 环境使用禁限表ID */
    readonly restriction_id: string;
    /** 是否正在使用 */
    readonly active: boolean;
}

/** 英文源数据「卡池」 */
interface PoolSchema extends BaseSchema {
    /** 卡池名称 */
    readonly name: string;
    /** 卡池所属环境ID */
    readonly format_id: string;
    /** 卡池包含循环ID */
    readonly card_cycle_ids: string[];
    /** 卡池包含卡包ID */
    readonly card_set_ids: string[];
}

/** 英文数据源「禁限表」 */
interface RestrictionSchema extends BaseSchema {
    /** 禁限表名称 */
    readonly name: string;
    /** 禁限表所属环境ID */
    readonly format_id: string;
    /** 禁限表开始日期 */
    readonly date_start: string;
    /** 禁限表禁止卡牌ID */
    readonly banned: string[];
    /** (暂不使用) */
    readonly restricted: string[];
    /** 禁限表禁止子类型ID */
    readonly subtypes: { readonly banned: string[]; };
    /** (暂不使用) */
    readonly universal_faction_cost: { readonly [key: string]: string[]; }
    /** (暂不使用) */
    readonly global_penalty: { readonly [key: string]: string[] };
    /** (暂不使用) */
    readonly points: { readonly [key: string]: string[] };
    /** (暂不使用) */
    readonly point_limit: number;
}

/** 英文源数据「卡牌」 */
interface CardSchema extends BaseSchema {
    /** 卡牌名称 */
    readonly title: string;
    /** 卡牌名称（ASCII） */
    readonly stripped_title: string;
    /** 卡牌文本 */
    readonly text: string;
    /** 卡牌文本（ASCII） */
    readonly stripped_text: string;
    /** 卡牌类型ID */
    readonly card_type_id: string;
    /** 卡牌子类型ID */
    readonly subtypes: string[];
    /** 卡牌阵营ID */
    readonly side_id: string;
    /** 卡牌派系ID */
    readonly faction_id: string;
    /** 卡牌是否独有 */
    readonly is_unique: boolean;
    /** 卡牌牌组限制 */
    readonly deck_limit: number | undefined;
    /** 卡牌推进需求 */
    readonly advancement_requirement: number | undefined;
    /** 卡牌议案分数 */
    readonly agenda_points: number | undefined;
    /** 卡牌基础中转 */
    readonly base_link: number | undefined;
    /** 卡牌牌组最小张数 */
    readonly minimum_deck_size: number | undefined;
    /** 卡牌牌组影响力上限 */
    readonly influence_limit: number | undefined;
    /** 卡牌影响力费用 */
    readonly influence_cost: number | undefined;
    /** 卡牌费用 */
    readonly cost: number | undefined;
    /** 卡牌强度 */
    readonly strength: number | undefined;
    /** 卡牌内存费用 */
    readonly memory_cost: number | undefined;
    /** 卡牌销毁费用 */
    readonly trash_cost: number | undefined;
    /** 卡牌布局 */
    readonly layout_id: "normal" | "flip" | "copy" | "facade" | "progression";
    /** 卡牌其它牌面 */
    readonly faces: {
        readonly title: string;
        readonly text: string;
    }[];

    /** 卡牌冠名 */
    readonly attribution: string;
    /** 卡牌设计组 */
    readonly designed_by: string;
    /** 卡牌人称代词 */
    readonly pronouns: string;
    /** 卡牌读音（国际音标） */
    readonly pronunciation_ipa: string;
    /** 卡牌读音（英文音标） */
    readonly pronunciation_approx: string;
}

/** 英文源数据「卡图」 */
interface PrintingSchema extends BaseSchema {
    /** 卡图卡牌ID */
    readonly card_id: string;
    /** 卡图所属卡包ID */
    readonly card_set_id: string;
    /** 卡图序号 */
    readonly position: number;
    /** 卡图风味文字 */
    readonly flavor: string;
    /** 卡图数量 */
    readonly quantity: number;
    /** 卡图牌面 */
    readonly faces: {
        readonly flavor: string;
    }[];
    /** 卡图插画作者 */
    readonly illustrator: string;
    /** 卡图发行组 */
    readonly released_by: string;
}

/** 英文源数据「FAQ」 */
interface RulingSchema extends BaseSchema {
    /** FAQ所属卡牌ID */
    readonly card_id: string;
    /** FAQ问题 */
    readonly question: string;
    /** FAQ答案 */
    readonly answer: string;
    /** FAQ文本规则 */
    readonly text_ruling: string;
    /** FAQ日期 */
    readonly date_update: string;
    /** FAQ验证性 */
    readonly nsg_rules_team_verified: boolean;
}


async function initialize(): Promise<void> {
    log.setLevel(log.levels.INFO);
    await AppDataSource.initialize();
    log.info(`SQLite database 'netrunner.sqlite' connected!`);
}

async function terminate(): Promise<void> {
    await AppDataSource.destroy();
}

async function load_schemas<T extends BaseSchema>(filename: string): Promise<Array<T>> {
    const result = new Array<T>();
    const stat = await fs.lstat(filename);
    if(stat.isDirectory()) {
        const files = await fs.readdir(filename);
        for(const f of files) {
            const subfolder = path.join(filename, f);
            const subordinates = await load_schemas<T>(subfolder);
            result.push(...subordinates);
        }
    } else if(stat.isFile()) {
        if(filename.endsWith(".json")) {
            const text = await fs.readFile(filename, "utf8");
            const content = JSON.parse(text);
            if(Array.isArray(content)) {
                const items = content as T[];
                for(const i of items) {
                    result.push(i);
                }
            } else {
                result.push(content as T);
            }
        }
    }

    return result;
}

async function extract_sides(): Promise<void> {
    const schemas = await load_schemas<SideSchema>("data/Oracle/v2/sides.json");
    const database = AppDataSource.getRepository(SideEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new SideEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        await database.save(record);
    }

    log.info("Save 'sides' finished!");
}

async function extract_factions(): Promise<void> {
    const schemas = await load_schemas<FactionSchema>("data/Oracle/v2/factions.json");
    const database = AppDataSource.getRepository(FactionEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new FactionEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.oracle_desc = schema.description ?? "";
        record.color = schema.color ?? "";
        record.is_mini = schema.is_mini;
        record.side_codename = schema.side_id ?? "";
        const side_entity = await AppDataSource.manager.findOneBy(SideEntity, { codename: record.side_codename });
        if(side_entity) {
            record.side = side_entity;
        }

        await database.save(record);
    }

    log.info("Save 'factions' finished!");
}

async function extract_types(): Promise<void> {
    const schemas = await load_schemas<TypeSchema>("data/Oracle/v2/card_types.json");
    const database = AppDataSource.getRepository(TypeEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new TypeEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.side_codename = schema.side_id ?? "";
        const side_entity = await AppDataSource.manager.findOneBy(SideEntity, { codename: record.side_codename });
        if(side_entity) {
            record.side = side_entity;
        }

        await database.save(record);
    }

    log.info("Save 'types' finished!");
}

async function extract_subtypes(): Promise<void> {
    const schemas = await load_schemas<SubtypeSchema>("data/Oracle/v2/card_subtypes.json");
    const database = AppDataSource.getRepository(SubtypeEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new SubtypeEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        await database.save(record);
    }

    log.info("Save 'subtypes' finished!");
}

async function extract_settypes(): Promise<void> {
    const schemas = await load_schemas<SettypeSchema>("data/Oracle/v2/card_set_types.json");
    const database = AppDataSource.getRepository(SettypeEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new SettypeEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.oracle_desc = schema.description ?? "";
        await database.save(record);
    }

    log.info("Save 'settypes' finished!");
}

async function extract_cycles(): Promise<void> {
    const schemas = await load_schemas<CycleSchema>("data/Oracle/v2/card_cycles.json");
    const database = AppDataSource.getRepository(CycleEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new CycleEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.position = schema.position ?? 0;
        record.released_by = schema.released_by ?? "";
        await database.save(record);
    }

    log.info("Save 'cycles' finished!");
}

async function extract_sets(): Promise<void> {
    const schemas = await load_schemas<SetSchema>("data/Oracle/v2/card_sets.json");
    const database = AppDataSource.getRepository(SetEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new SetEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.cycle_codename = schema.card_cycle_id ?? "";
        record.settype_codename = schema.card_set_type_id ?? "";
        record.release_date = schema.date_release ?? "";
        record.position = schema.position ?? 0;
        record.size = schema.size ?? 0;
        record.released_by = schema.released_by ?? "";

        const cycle_entity = await AppDataSource.manager.findOneBy(CycleEntity, { codename: record.cycle_codename });
        if(cycle_entity) {
            record.cycle = cycle_entity;
        }

        const settype_entity = await AppDataSource.manager.findOneBy(SettypeEntity, { codename: record.settype_codename });
        if(settype_entity) {
            record.settype = settype_entity;
        }

        await database.save(record);
    }

    log.info("Save 'sets' finished!");
}

async function extract_cards(): Promise<void> {
    const schemas = await load_schemas<CardSchema>("data/Oracle/v2/cards");
    const database = AppDataSource.getRepository(CardEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new CardEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_title = schema.title ?? "";
        record.stripped_title = schema.stripped_title ?? "";
        let oracle_text = schema.text ?? "";
        if(schema.faces && schema.faces.length > 0) {
            for(const face of schema.faces) {
                if(!face.text) {
                    continue;
                }

                const prefix = (schema.layout_id === "flip" ? "<strong>Back:</strong> " : "<strong>Side:</strong> ");
                const face_title = face.title ?? schema.title;
                const face_text = face.text;
                oracle_text = oracle_text + `\n${prefix}${face_title}\n${face_text}`;
            }
        }
        record.oracle_text = oracle_text;
        record.stripped_text = schema.stripped_text ?? "";
        record.type_codename = schema.card_type_id ?? "";
        record.subtypes = [];
        if(schema.subtypes && schema.subtypes.length > 0) {
            record.subtype_codenames = schema.subtypes.join(",");
            for(const subtype_codename of schema.subtypes) {
                const subtype_entity = await AppDataSource.manager.findOneBy(SubtypeEntity, { codename: subtype_codename });
                if(subtype_entity) {
                    record.subtypes.push(subtype_entity);
                }
            }
        }

        record.side_codename = schema.side_id ?? "";
        record.faction_codename = schema.faction_id ?? "";
        record.is_unique = !!schema.is_unique;
        record.deck_limit = schema.deck_limit;
        record.advancement_requirement = schema.advancement_requirement;
        record.agenda_point = schema.agenda_points;
        record.base_link = schema.base_link;
        record.minimum_deck_size = schema.minimum_deck_size;
        record.influence_limit = schema.influence_limit;
        record.influence_cost = schema.influence_cost;
        record.cost = schema.cost;
        record.strength = schema.strength;
        record.memory_cost = schema.memory_cost;
        record.trash_cost = schema.trash_cost;
        record.attribution = schema.attribution ?? "";
        record.designed_by = schema.designed_by ?? "";
        record.pronouns = schema.pronouns ?? "";
        record.pronunciation_ipa = schema.pronunciation_ipa ?? "";
        record.pronunciation_approx = schema.pronunciation_approx ?? "";
        record.extra_face = schema.faces ? schema.faces.length : 0;

        const type_entity = await AppDataSource.manager.findOneBy(TypeEntity, { codename: record.type_codename });
        if(type_entity) {
            record.type = type_entity;
        }

        const side_entity = await AppDataSource.manager.findOneBy(SideEntity, { codename: record.side_codename });
        if(side_entity) {
            record.side = side_entity;
        }

        const faction_entity = await AppDataSource.manager.findOneBy(FactionEntity, { codename: record.faction_codename });
        if(faction_entity) {
            record.faction = faction_entity;
        }

        await database.save(record);
    }

    log.info("Save 'cards' finished!");
}

async function extract_printings(): Promise<void> {
    const schemas = await load_schemas<PrintingSchema>("data/Oracle/v2/printings");
    const database = AppDataSource.getRepository(PrintingEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new PrintingEntity();
        }

        record.codename = schema.id ?? "";
        record.card_codename = schema.card_id ?? "";
        record.set_codename = schema.card_set_id ?? "";
        record.position = schema.position;
        let oracle_flavor = schema.flavor ?? "";
        if(schema.faces && schema.faces.length > 0) {
            for(const face of schema.faces) {
                if(face.flavor && face.flavor.length > 0) {
                    oracle_flavor = oracle_flavor + (oracle_flavor.length > 0 ? "\n" : "") + face.flavor;
                }
            }
        }
        record.oracle_flavor = oracle_flavor;
        record.quantity = schema.quantity ?? 0;
        record.extra_face = schema.faces ? schema.faces.length : 0;
        record.illustrator = schema.illustrator ?? "";
        record.released_by = schema.released_by ?? "";

        const card_entity = await AppDataSource.manager.findOneBy(CardEntity, { codename: record.card_codename });
        if(card_entity) {
            record.card = card_entity;
        }

        const set_entity = await AppDataSource.manager.findOneBy(SetEntity, { codename: record.set_codename });
        if(set_entity) {
            record.set = set_entity;
        }

        await database.save(record);
    }

    log.info("Save 'printings' finished!");
}

async function extract_rulings(): Promise<void> {
    const schemas = await load_schemas<RulingSchema>("data/Oracle/v2/rulings");
    const database = AppDataSource.getRepository(RulingEntity);
    await database.clear();
    for(const schema of schemas) {
        const record = new RulingEntity();
        record.card_codename = schema.card_id ?? "";
        record.question = schema.question ?? "";
        record.answer = schema.answer ?? "";
        record.text = schema.text_ruling ?? "";
        record.update_date = schema.date_update ?? "";
        record.nsg_verified = !!schema.nsg_rules_team_verified;

        const card_entity = await AppDataSource.manager.findOneBy(CardEntity, { codename: record.card_codename });
        if(card_entity) {
            record.card = card_entity;
        }

        await database.save(record);
    }

    log.info("Save 'rulings' finished!");
}

async function extract_formats(): Promise<void> {
    const schemas = await load_schemas<FormatSchema>("data/Oracle/v2/formats");
    const database = AppDataSource.getRepository(FormatEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new FormatEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        await database.save(record);
    }

    log.info("Save 'formats' finished!");
}

async function extract_pools(): Promise<void> {
    const schemas = await load_schemas<PoolSchema>("data/Oracle/v2/card_pools");
    const database = AppDataSource.getRepository(PoolEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new PoolEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.format_codename = schema.format_id ?? "";
        record.cycles = [];
        if(schema.card_cycle_ids && schema.card_cycle_ids.length > 0) {
            record.cycle_codenames = schema.card_cycle_ids.join(",");
            for(const cycle_codename of schema.card_cycle_ids) {
                const cycle_entity = await AppDataSource.manager.findOneBy(CycleEntity, { codename: cycle_codename });
                if(cycle_entity) {
                    record.cycles.push(cycle_entity);
                }
            }
        }

        record.sets = [];
        if(schema.card_set_ids && schema.card_set_ids.length > 0) {
            record.set_codenames = schema.card_set_ids.join(",");
            for(const set_codename of schema.card_set_ids) {
                const set_entity = await AppDataSource.manager.findOneBy(SetEntity, { codename: set_codename });
                if(set_entity) {
                    record.sets.push(set_entity);
                }
            }
        }

        const format_entity = await AppDataSource.manager.findOneBy(FormatEntity, { codename: record.format_codename });
        if(format_entity) {
            record.format = format_entity;
        }

        await database.save(record);
    }

    log.info("Save 'pools' finished!");
}

async function extract_restrictions(): Promise<void> {
    const schemas = await load_schemas<RestrictionSchema>("data/Oracle/v2/restrictions");
    const database = AppDataSource.getRepository(RestrictionEntity);
    for(const schema of schemas) {
        let record = await database.findOneBy({ codename: schema.id });
        if(!record) {
            record = new RestrictionEntity();
        }

        record.codename = schema.id ?? "";
        record.oracle_name = schema.name ?? "";
        record.format_codename = schema.format_id ?? "";
        record.start_date = schema.date_start ?? "";
        record.banned_cards = [];
        if(schema.banned && schema.banned.length > 0) {
            record.banned_card_codenames = schema.banned.join(",");
            for(const card_codename of schema.banned) {
                const card_entity = await AppDataSource.manager.findOneBy(CardEntity, { codename: card_codename });
                if(card_entity) {
                    record.banned_cards.push(card_entity);
                }
            }
        }

        record.banned_subtypes = [];
        if(schema.subtypes && schema.subtypes.banned && schema.subtypes.banned.length > 0) {
            record.banned_subtype_codenames = schema.subtypes.banned.join(",");
            for(const subtype_codename of schema.subtypes.banned) {
                const subtype_entity = await AppDataSource.manager.findOneBy(SubtypeEntity, { codename: subtype_codename });
                if(subtype_entity) {
                    record.banned_subtypes.push(subtype_entity);
                }
            }
        }

        const format_entity = await AppDataSource.manager.findOneBy(FormatEntity, { codename: record.format_codename });
        if(format_entity) {
            record.format = format_entity;
        }

        await database.save(record);
    }

    log.info("Save 'restrictions' finished!");
}

async function extract_snapshots(): Promise<void> {
    const schemas = await load_schemas<FormatSchema>("data/Oracle/v2/formats");
    const database = AppDataSource.getRepository(SnapshotEntity);
    for(const schema of schemas) {
        for(const member of schema.snapshots) {
            let record = await database.findOneBy({ codename: member.id });
            if(!record) {
                record = new SnapshotEntity();
            }

            record.codename = member.id ?? "";
            record.start_date = member.date_start ?? "";
            record.format_codename = schema.id ?? "";
            record.pool_codename = member.card_pool_id ?? "";
            record.restriction_codename = member.restriction_id ?? "";
            record.active = !!member.active;

            const format_entity = await AppDataSource.manager.findOneBy(FormatEntity, { codename: record.format_codename });
            if(format_entity) {
                record.format = format_entity;
            }

            const pool_entity = await AppDataSource.manager.findOneBy(PoolEntity, { codename: record.pool_codename });
            if(pool_entity) {
                record.pool = pool_entity;
            }

            const restriction_entity = await AppDataSource.manager.findOneBy(RestrictionEntity, { codename: record.restriction_codename });
            if(restriction_entity) {
                record.restriction = restriction_entity;
            }

            await database.save(record);
        }
    }

    log.info("Save 'snapshots' finished!");
}

async function main(): Promise<void> {
    await initialize();
    await extract_sides();
    await extract_factions();
    await extract_types();
    await extract_subtypes();
    await extract_settypes();
    await extract_cycles();
    await extract_sets();
    await extract_formats();
    await extract_pools();
    await extract_restrictions();
    await extract_snapshots();
    await extract_cards();
    await extract_printings();
    await extract_rulings();
}

main()
    .then(() => {
        log.info("Finished!");
    })
    .catch((err: Error) => {
        log.error("Failed with error: " + err.message);
        log.error("Stacktrace: " + err.stack);
    })
    .finally(async () => {
        await terminate();
    });
